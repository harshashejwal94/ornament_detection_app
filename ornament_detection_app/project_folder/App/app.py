import cv2
import face_recognition
import numpy as np
import streamlit as st
import os

st.set_page_config(page_title="Ornament detection App", page_icon=":smiley:")
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] {
        background-color: pink;
    }
    
    .stApp {
        background-color: #87CEEB;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)


def process_video(video_path, insert_image_path):
    # Create the output folder if it doesn't exist
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

  
    video_capture = cv2.VideoCapture(video_path)

    
    ret, frame = video_capture.read()

    
    resize_width = 400
    resize_height = 400

    
    frame_count = 0

    
    selected_frame_count = 0

    
    while ret and selected_frame_count < 5:  
        
        frame = cv2.resize(frame, (resize_width, resize_height))

        
        face_landmarks_list = face_recognition.face_landmarks(frame)

        
        if len(face_landmarks_list) > 0:
            face_landmarks = face_landmarks_list[0]  

            
            chin_landmarks = face_landmarks['chin']

            
            left_earlobe_point = chin_landmarks[1]  
            right_earlobe_point = chin_landmarks[-2]  

            
            points_below_left_earlobe = [point for point in chin_landmarks[1:3] if point[1] > left_earlobe_point[1]]
            points_below_right_earlobe = [point for point in chin_landmarks[-3:-1] if point[1] > right_earlobe_point[1]]

            
            insert_image = cv2.imread(insert_image_path, cv2.IMREAD_UNCHANGED)

            
            if insert_image.shape[2] == 4:
                
                insert_width = 50  
                insert_height = 100  
                insert_image = cv2.resize(insert_image, (insert_width, insert_height))

               
                alpha_channel = insert_image[:, :, 3] / 255.0

                
                insert_rgb = insert_image[:, :, :3]

               
                insert_x_left = points_below_left_earlobe[0][0] - insert_width // 2  
                insert_y_left = points_below_left_earlobe[0][1] 

                
                insert_x_right = points_below_right_earlobe[0][0] - insert_width // 2  
                insert_y_right = points_below_right_earlobe[0][1]  

                
                overlay_left = (1 - alpha_channel)[:, :, np.newaxis] * frame[insert_y_left:insert_y_left + insert_height, insert_x_left:insert_x_left + insert_width] + alpha_channel[:, :, np.newaxis] * insert_rgb
                frame[insert_y_left:insert_y_left + insert_height, insert_x_left:insert_x_left + insert_width] = overlay_left

                
                overlay_right = (1 - alpha_channel)[:, :, np.newaxis] * frame[insert_y_right:insert_y_right + insert_height, insert_x_right:insert_x_right + insert_width] + alpha_channel[:, :, np.newaxis] * insert_rgb
                frame[insert_y_right:insert_y_right + insert_height, insert_x_right:insert_x_right + insert_width] = overlay_right

            else:
                st.write("Insert image does not have an alpha channel.")

        else:
            st.write("No face landmarks found.")

        
        output_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
        cv2.imwrite(output_path, frame)

        
        st.image(frame, channels="BGR")

        
        frame_count += 1

        
        selected_frame_count += 1

        
        ret, frame = video_capture.read()

    
    video_capture.release()


menu = ["Home", "Display Images"]


choice = st.sidebar.selectbox("Menu", menu)


if choice == "Home":
    
    st.title("Home! Welcome to Ornament detection App")
    st.write("Welcome to the Home page! Upload Video and Jewellery to see the match")
    
    uploaded_video = st.file_uploader("Upload a video file", type=["mp4", "mov"])

    
    uploaded_insert_image = st.file_uploader("Upload an Ornament image", type=["png", "jpg"])

   
    if uploaded_video is not None and uploaded_insert_image is not None:
        
        with open("input_video.mp4", "wb") as file:
            file.write(uploaded_video.getvalue())

        
        with open("insert_image.png", "wb") as file:
            file.write(uploaded_insert_image.getvalue())

        
        process_video("input_video.mp4", "insert_image.png")

elif choice == "Display Images":
    
    st.title("Display Images")

    
    image_files = os.listdir("output")

    if len(image_files) > 0:
        
        selected_image = st.selectbox("Select an image to display", image_files)

        
        image_path = os.path.join("output", selected_image)
        image = cv2.imread(image_path)
        st.image(image, channels="BGR")

    else:
        st.write("No images found. Please process a video first.")
