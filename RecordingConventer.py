import obspython as obs
import os
import subprocess
import time
import threading
from datetime import datetime

# Default settings
SETTINGS = {
    "ffmpeg_path": "ffmpeg",
    "output_extension": "mp4",
    "delete_original": False,
    "custom_args": "",
    "process_recordings": True,
    "process_replays": True,
    "progress_group": True,
    "progress_interval": 2
}

def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")

def script_description():
    return """<center>
    <h2 style="color: #7289DA;">🎥 Recording Converter</h2>
    <p style="font-size: 14px; margin-top: -10px; color: #99AAB5;">Automatically convert recordings with <code>ffmpeg</code></p>
    
    <a href="https://github.com/FanaticExplorer/RecordingConverter" 
       style="color: #7289DA; text-decoration: none;">
       📁 GitHub
    </a>
    
    <a href="https://bento.me/fanaticexplorer" 
       style="color: #FF5E5B; text-decoration: none;">
       ❤️ Donate
    </a>
    </center>"""

def script_defaults(settings):
    for key, value in SETTINGS.items():
        if isinstance(value, bool):
            obs.obs_data_set_default_bool(settings, key, value)
        elif isinstance(value, (int, float)):
            obs.obs_data_set_default_double(settings, key, value)
        else:
            obs.obs_data_set_default_string(settings, key, value)

def script_properties(settings=None):
    props = obs.obs_properties_create()
    
    # Main Settings Group (FFmpeg and Format)
    main_group = obs.obs_properties_create()
    obs.obs_properties_add_group(props, "main_group", "Main Settings", obs.OBS_GROUP_NORMAL, main_group)
    
    # FFmpeg path
    ffmpeg_prop = obs.obs_properties_add_path(
        main_group,
        "ffmpeg_path",
        "FFmpeg path",
        obs.OBS_PATH_FILE,
        "Executable files (*.exe);;All files (*.*)",
        None
    )
    obs.obs_property_set_long_description(ffmpeg_prop, 
        "Path to FFmpeg executable. Required for conversion.\n"
        "Download from ffmpeg.org if not installed.\n"
        "As default, refers to FFmpeg in the PATH."
    )
    
    # Output format
    ext_list = obs.obs_properties_add_list(
        main_group,
        "output_extension",
        "Output format",
        obs.OBS_COMBO_TYPE_LIST,
        obs.OBS_COMBO_FORMAT_STRING
    )
    obs.obs_property_list_add_string(ext_list, "MP4 (Recommended)", "mp4")
    obs.obs_property_list_add_string(ext_list, "MOV (QuickTime)", "mov")
    obs.obs_property_list_add_string(ext_list, "MKV (Original)", "mkv")
    obs.obs_property_list_add_string(ext_list, "AVI (Uncompressed)", "avi")
    obs.obs_property_list_add_string(ext_list, "FLV (Flash)", "flv")
    obs.obs_property_list_add_string(ext_list, "TS (MPEG Transport Stream)", "ts")
    
    # Custom FFmpeg arguments
    custom_args_prop = obs.obs_properties_add_text(
        main_group,
        "custom_args",
        "Custom FFmpeg arguments",
        obs.OBS_TEXT_DEFAULT
    )
    obs.obs_property_set_long_description(custom_args_prop,
        "Additional FFmpeg arguments for custom encoding settings.\n"
        "Leave blank for default settings.")
    
    # Behavior Group
    behavior_group = obs.obs_properties_create()
    obs.obs_properties_add_group(props, "behavior_group", "Behavior", obs.OBS_GROUP_NORMAL, behavior_group)
    
    # File handling
    delete_prop = obs.obs_properties_add_bool(behavior_group, "delete_original", "Delete original after conversion")
    obs.obs_property_set_long_description(delete_prop, 
        "Automatically delete the original recording file after successful conversion.\n"
        "Only works when converting to a different format.")
    
    # What to process
    obs.obs_properties_add_bool(behavior_group, "process_recordings", "Convert regular recordings")
    obs.obs_properties_add_bool(behavior_group, "process_replays", "Convert replay buffer saves")
    
    # Progress Reporting Group
    progress_group = obs.obs_properties_create()
    obs.obs_properties_add_group(props, "progress_group", "Progress Reporting (in Script Log)", obs.OBS_GROUP_CHECKABLE, progress_group)
    
    obs.obs_properties_add_float_slider(
        progress_group,
        "progress_interval",
        "Update interval (s)",
        0.5,  # min
        5.0,  # max (more reasonable upper limit)
        0.5   # step
    )
    
    return props

def script_update(settings):
    for key in SETTINGS.keys():
        if isinstance(SETTINGS[key], bool):
            SETTINGS[key] = obs.obs_data_get_bool(settings, key)
        elif isinstance(SETTINGS[key], (int, float)):
            SETTINGS[key] = obs.obs_data_get_double(settings, key)
        else:
            SETTINGS[key] = obs.obs_data_get_string(settings, key)

def log_progress(filename, current_percent):
    """Logs conversion progress to OBS script log"""
    if not SETTINGS["progress_group"]:
        return
    
    progress_bar = "[" + "=" * int(current_percent/5) + ">" + " " * (20 - int(current_percent/5)) + "]"
    obs.script_log(obs.LOG_INFO, 
        f"[{get_timestamp()}] Converting {os.path.basename(filename)}: {progress_bar} {current_percent:.1f}%")

def convert_video(input_path, output_path, source_type):
    """Handles the conversion process with throttled progress updates"""
    try:
        input_path = os.path.normpath(input_path)
        output_path = os.path.normpath(output_path)
        
        # Skip if output exists and is newer than input
        if os.path.exists(output_path) and os.path.getmtime(output_path) > os.path.getmtime(input_path):
            obs.script_log(obs.LOG_INFO, f"[{get_timestamp()}] ⏩ Skipping {source_type} (already converted): {os.path.basename(input_path)}")
            return
        
        cmd = [
            SETTINGS["ffmpeg_path"],
            '-i', input_path,
            *SETTINGS["custom_args"].split(),
            output_path
        ]
        cmd = [arg for arg in cmd if arg.strip()]
        
        obs.script_log(obs.LOG_INFO, f"[{get_timestamp()}] 🚀 Converting {source_type}: {os.path.basename(input_path)}")
        
        # Get total duration
        probe_cmd = [
            SETTINGS["ffmpeg_path"],
            '-i', input_path,
            '-f', 'null', '-'
        ]
        probe = subprocess.run(
            probe_cmd,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW,
            text=True
        )
        
        total_duration = 0
        for line in probe.stderr.split('\n'):
            if "Duration:" in line:
                time_str = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = time_str.split(":")
                total_duration = float(h) * 3600 + float(m) * 60 + float(s)
                break
        
        # Start conversion with progress tracking
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        last_update_time = 0
        while True:
            output_line = process.stdout.readline()
            if output_line == '' and process.poll() is not None:
                break
                
            if "time=" in output_line:
                current_time = time.time()
                if current_time - last_update_time >= SETTINGS["progress_interval"]:
                    time_str = output_line.split("time=")[1].split()[0]
                    h, m, s = time_str.split(":")
                    current_duration = float(h) * 3600 + float(m) * 60 + float(s)
                    if total_duration > 0:
                        current_percent = (current_duration / total_duration) * 100
                        log_progress(input_path, current_percent)
                        last_update_time = current_time
        
        # Final 100% update
        if SETTINGS["progress_group"]:
            log_progress(input_path, 100)
            
        if process.returncode == 0:
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                if SETTINGS["delete_original"] and os.path.splitext(input_path)[1].lower() != os.path.splitext(output_path)[1].lower():
                    os.remove(input_path)
                    obs.script_log(obs.LOG_INFO, f"[{get_timestamp()}] ✅ Success! Removed original {source_type}")
                else:
                    obs.script_log(obs.LOG_INFO, f"[{get_timestamp()}] ✅ Success! Kept original {source_type}")
            else:
                obs.script_log(obs.LOG_WARNING, f"[{get_timestamp()}] ⚠️ No output file created")
        else:
            obs.script_log(obs.LOG_ERROR, f"[{get_timestamp()}] ❌ {source_type} conversion failed")
            
    except Exception as e:
        obs.script_log(obs.LOG_ERROR, f"[{get_timestamp()}] 💥 {source_type} conversion crashed: {str(e)}")

def handle_recording_stopped():
    if not SETTINGS["process_recordings"]:
        return
        
    time.sleep(1)  # Let OBS finalize file
    current_file = obs.obs_frontend_get_last_recording()
    if not current_file:
        obs.script_log(obs.LOG_WARNING, f"[{get_timestamp()}] 🔍 No recording file found")
        return
        
    output_ext = SETTINGS["output_extension"].lstrip(".")
    output_path = f"{os.path.splitext(current_file)[0]}.{output_ext}"
    
    # Skip if same format and not deleting original
    if os.path.splitext(current_file)[1].lower() == f".{output_ext.lower()}" and not SETTINGS["delete_original"]:
        obs.script_log(obs.LOG_INFO, f"[{get_timestamp()}] ⏩ Skipping {current_file} (same format)")
        return
    
    threading.Thread(
        target=convert_video,
        args=(current_file, output_path, "recording"),
        daemon=True
    ).start()

def handle_replay_saved():
    if not SETTINGS["process_replays"]:
        return
        
    time.sleep(1)  # Let OBS finalize file
    current_file = obs.obs_frontend_get_last_replay()
    if not current_file:
        obs.script_log(obs.LOG_WARNING, f"[{get_timestamp()}] 🔍 No replay file found")
        return
        
    output_ext = SETTINGS["output_extension"].lstrip(".")
    output_path = f"{os.path.splitext(current_file)[0]}.{output_ext}"
    
    # Skip if same format and not deleting original
    if os.path.splitext(current_file)[1].lower() == f".{output_ext.lower()}" and not SETTINGS["delete_original"]:
        obs.script_log(obs.LOG_INFO, f"[{get_timestamp()}] ⏩ Skipping {current_file} (same format)")
        return
    
    threading.Thread(
        target=convert_video,
        args=(current_file, output_path, "replay"),
        daemon=True
    ).start()

def on_event(event):
    if event == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        obs.script_log(obs.LOG_INFO, f"[{get_timestamp()}] 🎬 Recording stopped")
        handle_recording_stopped()
    elif event == obs.OBS_FRONTEND_EVENT_REPLAY_BUFFER_SAVED:
        obs.script_log(obs.LOG_INFO, f"[{get_timestamp()}] 🔄 Replay buffer saved")
        handle_replay_saved()

def script_load(settings):
    obs.obs_frontend_add_event_callback(on_event)
    obs.script_log(obs.LOG_INFO, f"[{get_timestamp()}] 🧰 Plugin loaded")

def script_unload():
    obs.obs_frontend_remove_event_callback(on_event)
    obs.script_log(obs.LOG_INFO, f"[{get_timestamp()}] 🧰 Plugin unloaded")