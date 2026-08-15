import json,sys,pathlib

if getattr(sys,'frozen',False):
    base_dir = pathlib.Path(sys.executable).parent
else: base_dir = pathlib.Path(__file__).parent
_config_file = base_dir / "config.json"

if not _config_file.exists():
    print("=== Sei-Chan 初始設定 ===")
    prompt = ["Discord機器人的Token", "RCON的密碼", "伺服器外網IP", "伺服器Log位置", "Discord頻道ID"]
    key = ["dc_token", "rcon_pw", "wan_ip", "log_path", "dc_id"]
    data = {k: input(f"{p}：") for k, p in zip(key, prompt)}
    _config_file.write_text(json.dumps(data,indent=4,ensure_ascii=False),encoding="utf-8")
    print("設定完成，已建立 config.json")
_data = json.loads(_config_file.read_text(encoding="utf-8"))

dc_token = _data.get("dc_token")
rcon_pw = _data.get("rcon_pw")
wan_ip = _data.get("wan_ip")
log_path = _data.get("log_path")
dc_id = _data.get("dc_id")