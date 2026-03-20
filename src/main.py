"""
Kivy Video Editor for Android
"""

import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from android.permissions import request_permissions, Permission
import threading

# Import your video processor (will reuse existing code)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.video_processor import VideoProcessor

# Set window size for desktop testing
Window.size = (400, 600)

class VideoEditorApp(App):
    def build(self):
        self.processor = VideoProcessor()
        self.title = "Video Editor"
        return Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    padding: 10
    spacing: 10
    
    BoxLayout:
        size_hint_y: 0.1
        Label:
            text: 'Video Editor'
            font_size: '24sp'
            bold: True
            color: 0.2, 0.6, 1, 1
    
    BoxLayout:
        size_hint_y: 0.1
        Button:
            text: 'Select Video'
            on_press: app.select_video()
    
    BoxLayout:
        size_hint_y: 0.1
        Label:
            id: video_label
            text: 'No video selected'
            color: 0.5, 0.5, 0.5, 1
    
    BoxLayout:
        size_hint_y: 0.1
        Spinner:
            id: operation_spinner
            text: 'Select Operation'
            values: ['Trim', 'Add Text', 'Change Speed', 'Extract Audio', 'Apply Filter']
            on_text: app.on_operation_select()
    
    BoxLayout:
        id: params_container
        orientation: 'vertical'
        size_hint_y: 0.3
    
    BoxLayout:
        size_hint_y: 0.1
        Button:
            text: 'Process'
            on_press: app.process_video()
    
    BoxLayout:
        size_hint_y: 0.1
        ProgressBar:
            id: progress_bar
            max: 100
            value: 0
    
    BoxLayout:
        size_hint_y: 0.1
        Label:
            id: status_label
            text: 'Ready'
            font_size: '14sp'
''')
    
    def select_video(self):
        """Open file chooser to select video"""
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView(
            filters=['*.mp4', '*.avi', '*.mov', '*.mkv'],
            path='/storage/emulated/0'
        )
        content.add_widget(filechooser)
        
        def on_submit(instance):
            if filechooser.selection:
                self.video_path = filechooser.selection[0]
                self.root.ids.video_label.text = f"Selected: {os.path.basename(self.video_path)}"
                self.root.ids.video_label.color = (0, 1, 0, 1)
                popup.dismiss()
        
        btn_layout = BoxLayout(size_hint_y=0.2)
        btn_layout.add_widget(Button(text='Cancel', on_press=lambda x: popup.dismiss()))
        btn_layout.add_widget(Button(text='Select', on_press=on_submit))
        content.add_widget(btn_layout)
        
        popup = Popup(title='Select Video', content=content, size_hint=(0.9, 0.9))
        popup.open()
    
    def on_operation_select(self):
        """Show parameters for selected operation"""
        operation = self.root.ids.operation_spinner.text
        params_container = self.root.ids.params_container
        params_container.clear_widgets()
        
        if operation == 'Trim':
            params_container.add_widget(Label(text='Start Time (seconds):'))
            start_input = TextInput(text='0', multiline=False, input_filter='float')
            params_container.add_widget(start_input)
            params_container.add_widget(Label(text='End Time (seconds):'))
            end_input = TextInput(text='10', multiline=False, input_filter='float')
            params_container.add_widget(end_input)
            self.params = {'start': start_input, 'end': end_input}
            
        elif operation == 'Add Text':
            params_container.add_widget(Label(text='Text to add:'))
            text_input = TextInput(text='Hello', multiline=False)
            params_container.add_widget(text_input)
            params_container.add_widget(Label(text='Position:'))
            position_spinner = Spinner(text='center', values=['center', 'top', 'bottom'])
            params_container.add_widget(position_spinner)
            self.params = {'text': text_input, 'position': position_spinner}
            
        elif operation == 'Change Speed':
            params_container.add_widget(Label(text='Speed Factor:'))
            speed_spinner = Spinner(text='1.0', values=['0.25', '0.5', '0.75', '1.0', '1.5', '2.0', '3.0', '4.0'])
            params_container.add_widget(speed_spinner)
            self.params = {'speed': speed_spinner}
            
        elif operation == 'Apply Filter':
            params_container.add_widget(Label(text='Filter Type:'))
            filter_spinner = Spinner(
                text='grayscale', 
                values=['grayscale', 'sepia', 'negative', 'blur', 'sharpen', 'edge_detect']
            )
            params_container.add_widget(filter_spinner)
            self.params = {'filter': filter_spinner}
    
    def update_progress(self, value, message):
        """Update progress bar and status"""
        self.root.ids.progress_bar.value = value
        self.root.ids.status_label.text = message
    
    def process_video(self):
        """Process video with selected operation"""
        if not hasattr(self, 'video_path'):
            self.show_popup('Error', 'Please select a video first')
            return
        
        operation = self.root.ids.operation_spinner.text
        
        def process_thread():
            try:
                if operation == 'Trim':
                    start = float(self.params['start'].text)
                    end = float(self.params['end'].text)
                    output = '/storage/emulated/0/trimmed_video.mp4'
                    success, result = self.processor.trim_video(
                        self.video_path, output, start, end,
                        lambda v, m: Clock.schedule_once(lambda dt: self.update_progress(v, m))
                    )
                    
                elif operation == 'Add Text':
                    text = self.params['text'].text
                    position = self.params['position'].text
                    output = '/storage/emulated/0/text_video.mp4'
                    success, result = self.processor.add_text_overlay(
                        self.video_path, output, text, position, 50, 'white', None,
                        lambda v, m: Clock.schedule_once(lambda dt: self.update_progress(v, m))
                    )
                    
                elif operation == 'Change Speed':
                    speed = float(self.params['speed'].text)
                    output = '/storage/emulated/0/speed_video.mp4'
                    success, result = self.processor.change_speed(
                        self.video_path, output, speed,
                        lambda v, m: Clock.schedule_once(lambda dt: self.update_progress(v, m))
                    )
                    
                elif operation == 'Apply Filter':
                    filter_type = self.params['filter'].text
                    output = '/storage/emulated/0/filtered_video.mp4'
                    success, result = self.processor.apply_filter(
                        self.video_path, output, filter_type, 1.0,
                        lambda v, m: Clock.schedule_once(lambda dt: self.update_progress(v, m))
                    )
                
                elif operation == 'Extract Audio':
                    output = '/storage/emulated/0/extracted_audio.mp3'
                    success, result = self.processor.extract_audio(
                        self.video_path, output,
                        lambda v, m: Clock.schedule_once(lambda dt: self.update_progress(v, m))
                    )
                
                Clock.schedule_once(lambda dt: self.update_progress(100, 'Complete!'))
                Clock.schedule_once(lambda dt: self.show_popup('Success', f'Video saved to {output}'))
                
            except Exception as e:
                Clock.schedule_once(lambda dt: self.show_popup('Error', str(e)))
        
        thread = threading.Thread(target=process_thread)
        thread.start()
    
    def show_popup(self, title, message):
        """Show a popup message"""
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        btn = Button(text='OK', size_hint_y=0.3)
        content.add_widget(btn)
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        btn.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    # Request permissions for Android
    try:
        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
    except:
        pass
    VideoEditorApp().run()