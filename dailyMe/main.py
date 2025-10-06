import customtkinter as ctk
import tkinter.font as tkFont
import json, os
from datetime import date, datetime, timedelta
from PIL import Image, ImageTk
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog

root = ctk.CTk()

mainFont = ctk.CTkFont(family="Itim-Regular", size=18)
secondFont = ctk.CTkFont(family="Itim-Regular", size=14)

root.title("Save A My Useless Day")
root.geometry("325x600")

notebook = ctk.CTkTabview(root)
notebook.pack(expand=True, fill="both")

tab = notebook.add("Daily")
tab2 = notebook.add("Files")
tab3 = notebook.add("Questions")

dailyFrame = ctk.CTkFrame(tab)
dailyFrame.pack(expand=True, fill="both", padx=10, pady=10, ipadx=10, ipady=10)
dailyFrame.grid_columnconfigure(0, weight=1)

dateFrame = ctk.CTkFrame(dailyFrame)
dateFrame.grid(row=0, column=0, columnspan=3)
dateFrame.grid_columnconfigure(0, weight=1)

writeScrollFrame = ctk.CTkScrollableFrame(dailyFrame, height=280)
writeScrollFrame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=15)
writeScrollFrame.grid_columnconfigure(0, weight=1)


def checkFormatTime():
    if not entryDate.get():
        CTkMessagebox(title="Error", message="Please enter a date.", icon="cancel")
        return False
    # Check date format ถูกไหม
    try:
        datetime.strptime(entryDate.get(), "%d/%m/%Y")
        return True
    except ValueError:
        CTkMessagebox(title="Error", message="Please enter the date in DD/MM/YYYY format.", icon="cancel")
        return False

def changeDate(value):
    if not checkFormatTime():
        return
    current_date_str = entryDate.get()
    current_date = datetime.strptime(current_date_str, "%d/%m/%Y").date()
    new_date = current_date + timedelta(days=value)
    entryDate.delete(0, ctk.END)
    entryDate.insert(0, new_date.strftime("%d/%m/%Y"))




prevButton = ctk.CTkButton(dateFrame, text="<", font=secondFont, width=50, command=lambda: changeDate(-1))
prevButton.grid(row=0, column=2, pady=5)

entryDate = ctk.CTkEntry(dateFrame, font=secondFont, width=120)
entryDate.grid(row=0, column=3, pady=5)
entryDate.insert(0, date.today().strftime("%d/%m/%Y"))

nextButton = ctk.CTkButton(dateFrame, text=">", font=secondFont, width=50, command=lambda: changeDate(1))
nextButton.grid(row=0, column=4, pady=5)




label1 = ctk.CTkLabel(writeScrollFrame, font=mainFont, text="วันนี้รู้สึกยังไงบ้าง?")
label1.grid(row=0, column=0, columnspan=2, pady=5)

textarea1 = ctk.CTkTextbox(writeScrollFrame, font=mainFont, height=66)
textarea1.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

label2 = ctk.CTkLabel(writeScrollFrame, font=mainFont, text="ตอนนี้คิดถึงเรื่องอะไรบ่อยที่สุด?")
label2.grid(row=2, column=0, columnspan=3, pady=5)

textarea2 = ctk.CTkTextbox(writeScrollFrame, font=mainFont, height=66)
textarea2.grid(row=3, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

loaded_data = {}
label_list = []
tags_list = []
textarea_list = []
created_emotion = False
rowCount = 3

path = os.path.dirname(os.path.abspath(__file__))
selected_emotion = []
def reload_json():
    global loaded_data
    if os.path.exists(f"{path}/option.json"):
        with open(f"{path}/option.json", "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
reload_json()

def load_daily():
    reload_json()
    global rowCount
    global created_emotion
    display_info = loaded_data["display"]
    for label in label_list:
        label.destroy()
    for textarea in textarea_list:
        textarea.destroy()

    label_list.clear()
    textarea_list.clear()
    for question, data in display_info.items():
        # Only add questions that are activated
        if data['activate'] == True:
            rowCount += 1
            label = ctk.CTkLabel(writeScrollFrame, font=mainFont, text=data['text'])
            label.grid(row=rowCount, column=0, columnspan=3, pady=5)
            label_list.append(label)

            tags_list.append(data['key'])

            rowCount += 1
            textarea = ctk.CTkTextbox(writeScrollFrame, font=mainFont, height=66)
            textarea.grid(row=rowCount, columnspan=3, column=0, sticky="ew", padx=5, pady=5)
            textarea_list.append(textarea)
    # Reset selected_emotion when reloading daily questions
    selected_emotion.clear()

    if not created_emotion:
        created_emotion = True
        rowCount += 1
        emotionFrame = ctk.CTkFrame(dailyFrame, height=60)
        emotionFrame.grid(row=rowCount, column=0, columnspan=3, ipady=10,sticky="ew")

        emotionFrame.grid_columnconfigure(0, weight=1)
        emotionFrame.grid_columnconfigure(1, weight=1)
        emotionFrame.grid_columnconfigure(2, weight=1)
        emotionFrame.grid_columnconfigure(3, weight=1)
        emotionFrame.grid_columnconfigure(4, weight=1)

        emotion_label = ctk.CTkLabel(emotionFrame, font=mainFont, text="อารมณ์วันนี้:")
        emotion_label.grid(row=0, column=0, columnspan=9, pady=5)
        emotion_data = loaded_data["emotion"]
        emotion_buttons = []

        for name, emotion_info in emotion_data.items():
            # Function to handle button click for multiple selections
            def on_emotion_click(clicked_button, emotion_name):
                if emotion_name in selected_emotion:
                    # If already selected, deselect it
                    selected_emotion.remove(emotion_name)
                    clicked_button.configure(fg_color="transparent")
                else:
                    # If not selected, select it
                    selected_emotion.append(emotion_name)
                    clicked_button.configure(fg_color="#3B8ED0")

                print(f"Selected emotion: {emotion_name}") # For debugging or further action
            # Load image for the button
            image_path = os.path.join(path, "assets", emotion_info['image'])
            button_image = ctk.CTkImage(Image.open(image_path), size=(30, 30))

            button = ctk.CTkButton(emotionFrame, text=emotion_info['text'], font=secondFont, fg_color="transparent",
                                    image=button_image, compound="top", width=50, height=30)
            button.grid(row=1, column=emotion_info['index'] - 1, padx=2, pady=5)

            # Add hover effect
            def on_enter(event, btn, original_image, hover_image):
                btn.configure(image=hover_image)

            def on_leave(event, btn, original_image):
                btn.configure(image=original_image)

            # Create a larger image for hover effect
            hover_button_image = ctk.CTkImage(Image.open(image_path), size=(35, 35))

            button.bind("<Enter>", lambda event, b=button, oi=button_image, hi=hover_button_image: on_enter(event, b, oi, hi))
            button.bind("<Leave>", lambda event, b=button, oi=button_image: on_leave(event, b, oi))
            button.configure(command=lambda b=button, n=name: on_emotion_click(b, n))

            emotion_buttons.append(button)

fileSaveType = ["txt", "json"]
def save_data():
    if not checkFormatTime():
        return
    
    data = {
        "date": entryDate.get(),
        "feeling_today": textarea1.get("1.0", "end-1c"),
        "thinking_about": textarea2.get("1.0", "end-1c")
    }
    for i, label_widget in enumerate(label_list):
        question_text = label_widget.cget("text")
        answer_text = textarea_list[i].get("1.0", "end-1c")
        data[tags_list[i]] = answer_text
    
    if selected_emotion:
        data["emotions"] = selected_emotion
        
    save_directory = ""
    try:
        defaultPath = loaded_data["setting"]["defaultPath"]
        if defaultPath == "":
            save_directory = os.path.join(path, 'data')
        else:
            save_directory = defaultPath
        os.makedirs(save_directory, exist_ok=True)
    except KeyError:
        # Handle 'defaultPath' might not exist
        CTkMessagebox(title="Error", message="Default save path not configured. Please check your option.json file.", icon="cancel")
        return
    except Exception as e:
        CTkMessagebox(title="Error", message=f"An error occurred while creating the directory: {e}", icon="cancel")
        return
    prefix = loaded_data.get("setting", {}).get("defaultPrefixName", "daily_")
    askbeforesave = loaded_data.get("setting", {}).get("askBeforeSave", True)
    save_file_path = f"{prefix}{date.today().strftime('%Y%m%d')}.{buttonType.cget('text')}"
    def saveFile():
        if buttonType.cget("text") == "json":
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        elif buttonType.cget("text") == "txt":
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"Date: {entryDate.get()}\n\n")
                f.write(f"วันนี้รู้สึกยังไงบ้าง?\n{textarea1.get('1.0', 'end-1c')}\n\n")
                f.write(f"ตอนนี้คิดถึงเรื่องอะไรบ่อยที่สุด?\n{textarea2.get('1.0', 'end-1c')}\n\n")
                
                for i, label_widget in enumerate(label_list):
                    question_text = label_widget.cget("text")
                    answer_text = textarea_list[i].get("1.0", "end-1c")
                    f.write(f"{question_text}\n{answer_text}\n\n")

                # Add selected emotions
                if selected_emotion:
                    f.write(f"อารมณ์วันนี้: {', '.join(selected_emotion)}\n\n")
    
    if askbeforesave:
        choice_file_path = filedialog.asksaveasfilename(
            title="Save File",
            defaultextension=f".{buttonType.cget('text')}",
            filetypes=[(f"{buttonType.cget('text').upper()} files", f"*.{buttonType.cget('text')}"), ("All files", "*.*")],
            initialdir=save_directory,
            initialfile=save_file_path
        )
        if not choice_file_path: # If user clicks No or closes the dialog
            return
        
        global file_path
        file_path = choice_file_path
        saveFile()
            
    else:

        file_path = os.path.join(save_directory, save_file_path)
        if os.path.exists(file_path):
            msg = CTkMessagebox(title="Confirm Overwrite", message="A file for today already exists. Do you want to overwrite it?",
                                icon="question", option_1="Cancel", option_2="Overwrite")
            if msg.get() == "Cancel":
                return
            saveFile()
      
        else:
            saveFile()
           
        
    msg2 = CTkMessagebox(title="Success", message=f"Data will be saved to: {file_path}", icon="check"
                  , option_1="Open File", option_2="Okay", option_3="Open Folder")
    if msg2.get() == "Okay":
        return
    elif msg2.get() == "Open File":
        try:
            os.startfile(file_path)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Could not open file: {e}", icon="cancel")
    elif msg2.get() == "Open Folder":
        try:
            os.startfile(save_directory)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Could not open folder: {e}", icon="cancel")
    return
    


def changeType():
    newType = fileSaveType[(fileSaveType.index(buttonType._text) + 1) % len(fileSaveType)]
    buttonType.configure(text=newType)
    pass




saveFileFrame = ctk.CTkFrame(dailyFrame)
saveFileFrame.grid(row=99, column=0, columnspan=3, pady=5)


buttonTypelabel = ctk.CTkLabel(saveFileFrame, font=mainFont, text="ประเภทไฟล์:")
buttonTypelabel.grid(row=rowCount, column=0, sticky="w", padx=5)

buttonType = ctk.CTkButton(saveFileFrame, text="txt", font=mainFont, command=changeType, width=50, fg_color="#6B6B6B", hover_color="#4F5357")
buttonType.grid(row=rowCount, column=1, pady=5, padx=5)

button1 = ctk.CTkButton(saveFileFrame, text="บันทึก", font=mainFont, command=save_data)
button1.grid(row=rowCount, column=2, pady=5)


# tab2 - Files
filesFrame = ctk.CTkFrame(tab2)
filesFrame.pack(expand=True, fill="both", padx=10, pady=10, ipadx=10, ipady=10)
filesFrame.grid_columnconfigure(0, weight=1)

file_path_label = ctk.CTkLabel(filesFrame, font=mainFont, text="ตำแหน่งบันทึกไฟล์:")
file_path_label.grid(row=0, column=0, pady=5, padx=5, sticky="w", columnspan=3)

file_path_label2 = ctk.CTkLabel(filesFrame, font=secondFont, text="ไม่มี", wraplength=150)
file_path_label2.grid(row=0, column=3, pady=5, padx=5, sticky="w")

file_path_entry = ctk.CTkEntry(filesFrame, font=secondFont, width=120)
file_path_entry.grid(row=1, column=0, pady=5,padx=5, sticky="ew", columnspan=3)

file_path_button = ctk.CTkButton(filesFrame, text="เลือกตำแหน่ง", width=40, font=secondFont, command=lambda: select_folder_and_update_path(file_path_entry, file_path_label))
file_path_button.grid(row=1, column=3, pady=5, padx=5, sticky="ew", columnspan=1)

def select_folder_and_update_path(entry_widget, label_widget):
    folder_selected = ctk.filedialog.askdirectory(initialdir=path if os.path.exists(path) else '/')
    if folder_selected:
        entry_widget.delete(0, ctk.END)
        entry_widget.insert(0, folder_selected)
        label_widget.configure(text=f"ตำแหน่งบันทึกไฟล์: {folder_selected}")
        update_default_path(folder_selected)

def update_default_path(new_path):
    global loaded_data
    try:
        if "setting" not in loaded_data:
            loaded_data["setting"] = {}
        loaded_data["setting"]["defaultPath"] = new_path
        
        with open(f"{path}/option.json", "w", encoding="utf-8") as f:
            json.dump(loaded_data, f, ensure_ascii=False, indent=4)
        CTkMessagebox(title="Success", message="Default save path updated successfully!", icon="check")
    except Exception as e:
        CTkMessagebox(title="Error", message=f"Failed to update default path: {e}", icon="cancel")
    with open(f"{path}/option.json", "r", encoding="utf-8") as f:
        loaded_data = json.load(f)

def update_default_save_name():
    dialog = ctk.CTkInputDialog(text="ใส่ชื่อไฟล์เริ่มต้น (Prefix):", title="เปลี่ยนชื่อไฟล์เริ่มต้น")
    dialog.after(100, lambda: dialog._entry.insert(0, loaded_data["setting"]["defaultPrefixName"]))
    new_name = dialog.get_input()
    if new_name:
        loaded_data["setting"]["defaultPrefixName"] = new_name
        try:
            with open(f"{path}/option.json", "w", encoding="utf-8") as f:
                json.dump(loaded_data, f, ensure_ascii=False, indent=4)
                CTkMessagebox(title="Success", message="Default save name updated successfully!", icon="check")
                file_name_label2.configure(text=new_name)
        except Exception as e:
            CTkMessagebox(title="Error", message=f"Failed to update default save name: {e}", icon="cancel")


# # Initialize the file path display
if "setting" in loaded_data and "defaultPath" in loaded_data["setting"] and loaded_data["setting"]["defaultPath"]:
    default_path = loaded_data["setting"]["defaultPath"]
else:
    default_path = os.path.join(path, "data")

def shorten_path(path, max_parts=3):
    """
    ตัด path ให้เหลือแค่ส่วนท้ายสุด N ส่วน เช่น max_parts=3
    'C:/Users/PlayGaming/Documents/Projects/MyApp/data'
    → .../Projects/MyApp/data
    """
    parts = os.path.normpath(path).split(os.sep)
    if len(parts) > max_parts:
        return os.sep.join(["...", *parts[-max_parts:]])
    return path

file_path_entry.insert(0, default_path)
file_path_label2.configure(text=shorten_path(default_path, max_parts=2))


file_name_label = ctk.CTkLabel(filesFrame, font=mainFont, text="ชื่อไฟล์เริ่มต้น :")
file_name_label.grid(row=2, column=0, columnspan=2, pady=5)

file_name_label2 = ctk.CTkLabel(filesFrame, font=secondFont, text=loaded_data["setting"]["defaultPrefixName"], wraplength=150)
file_name_label2.grid(row=2, column=2, columnspan=5, pady=5, padx=5, sticky="w")

change_file_name_button = ctk.CTkButton(filesFrame, text="เปลี่ยนชื่อไฟล์เริ่มต้น", font=secondFont, command=update_default_save_name)
change_file_name_button.grid(row=3, column=0, columnspan=4, pady=5)

def toggle_ask_before_save(var):
    global loaded_data
    try:
        if "setting" not in loaded_data:
            loaded_data["setting"] = {}
        loaded_data["setting"]["askBeforeSave"] = var.get()
        
        with open(f"{path}/option.json", "w", encoding="utf-8") as f:
            json.dump(loaded_data, f, ensure_ascii=False, indent=4)
        # CTkMessagebox(title="Success", message="Ask before save setting updated.", icon="check")
    except Exception as e:
        CTkMessagebox(title="Error", message=f"Failed to update setting: {e}", icon="cancel")

ask_before_save_label = ctk.CTkLabel(filesFrame, font=mainFont, text="ถามก่อนบันทึกไฟล์:")
ask_before_save_label.grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

initial_ask_before_save = loaded_data.get("setting", {}).get("askBeforeSave", True) # Default to True
ask_before_save_var = ctk.BooleanVar(value=initial_ask_before_save)
ask_before_save_switch = ctk.CTkSwitch(filesFrame, text="", variable=ask_before_save_var, width=30,
                                    command=lambda var=ask_before_save_var: toggle_ask_before_save(var))
ask_before_save_switch.grid(row=4, column=2, padx=(5, 0), sticky="e")

    

separator = ctk.CTkFrame(filesFrame, height=2, fg_color="gray")
separator.grid(row=5, column=0, columnspan=4, sticky="ew", pady=10)

files_label = ctk.CTkLabel(filesFrame, font=mainFont, text="บันทึกทั้งหมด")
files_label.grid(row=5, column=0, columnspan=4, pady=5)

files_listbox = ctk.CTkTextbox(filesFrame, font=secondFont, height=200, width=280)
files_listbox.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

def load_files():
    files_listbox.delete("1.0", "end")
    try:
        defaultPath = loaded_data["setting"]["defaultPath"]
        if defaultPath == "":
            save_directory = os.path.join(path, 'data')
        else:
            save_directory = defaultPath
        
        if not os.path.exists(save_directory):
            files_listbox.insert("end", "No saved entries yet.")
            return

        files = [f for f in os.listdir(save_directory) if os.path.isfile(os.path.join(save_directory, f))]
        if not files:
            files_listbox.insert("end", "No saved entries yet.")
            return

        for f in sorted(files, reverse=True):
            files_listbox.insert("end", f + "\n")
    except KeyError:
        files_listbox.insert("end", "Error: Default save path not configured.")
    except Exception as e:
        files_listbox.insert("end", f"Error loading files: {e}")

def open_selected_file():
    selected_line = files_listbox.get("insert linestart", "insert lineend").strip()
    if not selected_line:
        CTkMessagebox(title="Error", message="Please select a file to open.", icon="cancel")
        return
    
    try:
        defaultPath = loaded_data["setting"]["defaultPath"]
        if defaultPath == "":
            save_directory = os.path.join(path, 'data')
        else:
            save_directory = defaultPath
        
        file_path = os.path.join(save_directory, selected_line)
        
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            CTkMessagebox(title="Error", message="Selected file not found.", icon="cancel")
    except KeyError:
        CTkMessagebox(title="Error", message="Default save path not configured.", icon="cancel")
    except Exception as e:
        CTkMessagebox(title="Error", message=f"Error opening file: {e}", icon="cancel")

files_listbox.bind("<Double-Button-1>", lambda event: open_selected_file())


load_files_button = ctk.CTkButton(filesFrame, text="Refresh Files", font=secondFont, command=load_files)
load_files_button.grid(row=7, column=0, columnspan=4, pady=5)

# เพิ่มคำถาม
def add_question():
    global rowCount
    global loaded_data
    
    dialog = ctk.CTkInputDialog(text="ใส่คำถามที่คุณต้องการเพิ่ม:", title="เพิ่มคำถาม")
    new_question_text = dialog.get_input()
    if not new_question_text:
        return # User cancelled or entered empty text

    dialog_key = ctk.CTkInputDialog(text="ใส่ Key Tag สำหรับคำถามนี้ (เป็นภาษาอังกฤษ, ไม่บังคับ):", title="Key Tag")
    new_question_key_tag = dialog_key.get_input()

    if not new_question_key_tag:
        # Generate a simple English tag from the question text if not provided
        new_question_key_tag = new_question_text.replace(" ", "_").replace("?", "").replace("!", "").lower()
    
    # Check if the tag already exists
    if new_question_key_tag in loaded_data["display"]:
        CTkMessagebox(title="Error", message="Key Tag นี้มีอยู่แล้ว", icon="cancel")
        return

    # Add new question to loaded_data
    loaded_data["display"][new_question_key_tag] = {
        "text": new_question_text,
        "key": new_question_key_tag,
        "activate": True
    }

    # Save updated data to option.json
    try:
        with open(f"{path}/option.json", "w", encoding="utf-8") as f:
            json.dump(loaded_data, f, ensure_ascii=False, indent=4)
        CTkMessagebox(title="Success", message="เพิ่มคำถามเรียบร้อยแล้ว! กรุณารีสตาร์ทแอปพลิเคชันเพื่อดูการเปลี่ยนแปลง", icon="check")
    except Exception as e:
        CTkMessagebox(title="Error", message=f"ไม่สามารถบันทึกคำถามได้: {e}", icon="cancel")

# Call load_files initially to populate the listbox when the app starts

def on_tab_change():
    if notebook.get() == "Files":
        load_files()
    elif notebook.get() == "Questions":
        load_questions()
    elif notebook.get() == "Daily":
        load_daily()
        pass


notebook.configure(command=on_tab_change)

# tab3 - Question
questionFrame = ctk.CTkFrame(tab3)
questionFrame.pack(expand=True, fill="both", padx=10, pady=10, ipadx=10, ipady=10)
questionFrame.grid_columnconfigure(0, weight=1)

question_list_frame = ctk.CTkScrollableFrame(questionFrame, height=150)
question_list_frame.grid(row=0, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

def load_questions():
    for widget in question_list_frame.winfo_children():
        widget.destroy()
    
    if "display" in loaded_data:
        for q_tag, q_info in loaded_data["display"].items():
            question_row_frame = ctk.CTkFrame(question_list_frame, fg_color="transparent")
            question_row_frame.pack(fill="x", pady=2)
            question_row_frame.grid_columnconfigure(0, weight=1)

            def edit_question(original_tag, current_text):
                dialog = ctk.CTkInputDialog(text="แก้ไขคำถาม:", title="แก้ไขคำถาม")
                dialog.after(100, lambda: dialog._entry.insert(0, current_text))
                new_text = dialog.get_input()
                if not new_text:
                    return # User cancelled or entered empty text

                dialog_key = CTkMessagebox(title="แก้ไข Key Tag", message="คุณต้องการแก้ไข Key Tag ของคำถามนี้ด้วยหรือไม่?",
                                           icon="question", option_1="ไม่", option_2="ใช่")
                new_tag = original_tag
                if dialog_key.get() == "ใช่":
                    dialog_key_input = ctk.CTkInputDialog(text=f"แก้ไข Key Tag (ปัจจุบัน: {original_tag}):", title="แก้ไข Key Tag")
                    dialog_key_input.after(100, lambda: dialog_key_input._entry.insert(0, original_tag))
                    new_tag_input = dialog_key_input.get_input()
                    if new_tag_input:
                        new_tag = new_tag_input

                if new_text != current_text or new_tag != original_tag:
                    if new_tag != original_tag:
                        del loaded_data["display"][original_tag] # Remove old entry
                    loaded_data["display"][new_tag] = {"text": new_text, "key": new_tag, "activate": True}
                    try:
                        with open(f"{path}/option.json", "w", encoding="utf-8") as f:
                            json.dump(loaded_data, f, ensure_ascii=False, indent=4)
                        CTkMessagebox(title="Success", message="คำถามและ/หรือ Key Tag ถูกแก้ไขแล้ว! กรุณารีสตาร์ทแอปพลิเคชันเพื่อดูการเปลี่ยนแปลง", icon="check")
                        load_questions() # Refresh the list
                    except Exception as e:
                        CTkMessagebox(title="Error", message=f"ไม่สามารถแก้ไขคำถามได้: {e}", icon="cancel")
            question_text_button = ctk.CTkButton(question_row_frame, font=secondFont, text=q_info["text"], anchor="w", fg_color="transparent", hover_color="#3B8ED0"
                                                 ,command=lambda tag=q_tag, text=q_info["text"]: edit_question(tag, text))
            question_text_button.grid(row=0, column=0, columnspan=2, sticky="ew")






            switch_var = ctk.BooleanVar(value=q_info["activate"])
            
            def toggle_question_activation(tag, var):
                loaded_data["display"][tag]["activate"] = var.get()
                try:
                    with open(f"{path}/option.json", "w", encoding="utf-8") as f:
                        json.dump(loaded_data, f, ensure_ascii=False, indent=4)
                    # CTkMessagebox(title="Success", message="สถานะคำถามอัปเดตแล้ว! กรุณารีสตาร์ทแอปพลิเคชันเพื่อดูการเปลี่ยนแปลง", icon="check")
                except Exception as e:
                    CTkMessagebox(title="Error", message=f"ไม่สามารถอัปเดตสถานะคำถามได้: {e}", icon="cancel")



            def delete_question(tag):
                msg = CTkMessagebox(title="Confirm Delete", message="Are you sure you want to delete this question?",
                                    icon="question", option_1="Cancel", option_2="Delete") 
                if msg.get() == "Delete":
                    del loaded_data["display"][tag]
                    try:
                        with open(f"{path}/option.json", "w", encoding="utf-8") as f:
                            json.dump(loaded_data, f, ensure_ascii=False, indent=4)
                        CTkMessagebox(title="Success", message="คำถามถูกลบแล้ว! กรุณารีสตาร์ทแอปพลิเคชันเพื่อดูการเปลี่ยนแปลง", icon="check")
                        load_questions() # Refresh the list
                    except Exception as e:
                        CTkMessagebox(title="Error", message=f"ไม่สามารถลบคำถามได้: {e}", icon="cancel")
            action_frame = ctk.CTkFrame(question_row_frame, fg_color="transparent")
            action_frame.grid(row=0, column=3, sticky="e")
            

            activation_switch = ctk.CTkSwitch(action_frame, text="", variable=switch_var, width=30,
                                              command=lambda tag=q_tag, var=switch_var: toggle_question_activation(tag, var))
            activation_switch.grid(row=0, column=3, padx=(5, 0), sticky="e")

            delete_button = ctk.CTkButton(action_frame, text="ลบ", font=secondFont, width=40, fg_color="red", hover_color="#8B0000",
                                          command=lambda tag=q_tag: delete_question(tag))
            delete_button.grid(row=0, column=4)
    else:
        no_questions_label = ctk.CTkLabel(question_list_frame, font=secondFont, text="No custom questions added yet.")
        no_questions_label.pack(pady=10)

load_questions_button = ctk.CTkButton(questionFrame, text="จัดการคำถาม", font=secondFont, command=load_questions)
load_questions_button.grid(row=1, column=0, columnspan=2, pady=5)

add_question_button = ctk.CTkButton(questionFrame, text="เพิ่มคำถาม", font=secondFont, command=add_question)
add_question_button.grid(row=1, column=2, columnspan=3, pady=5)
root.after(100, load_files)
root.after(100, load_questions)
root.after(100, load_daily)

# button1 = tk.Button(dailyFrame, text="บันทึก", font=mainFont)
# button1.grid(row=2, column=0, columnspan=2, pady=5)

"""
มีอะไรอยากจำไว้ หรืออยากลืมไปบ้าง?
อยากให้พรุ่งนี้ต่างจากวันนี้ยังไง?
มีอะไรทำให้ยิ้มหรือหงุดหงิดไหม?

"""

root.mainloop()