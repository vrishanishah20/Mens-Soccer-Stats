import streamlit as st
import tempfile
import os
from video_analyzer import SoccerVideoAnalyzer
def main():
    st.set_page_config(
        page_title="Soccer Match Analyzer",
        page_icon="⚽",
        layout="wide"
    )

    st.title("⚽ Soccer Match Video Analyzer")
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        api_key = st.text_input("OpenAI API Key:", type="password")
        
        st.header("About")
        st.write("""
        This app provides advanced soccer match analysis using AI:
        - Team positioning analysis
        - Key play identification
        - Player movement patterns
        - Tactical recommendations
        """)

    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload Video")
        uploaded_file = st.file_uploader(
            "Choose a video file (MP4, AVI, MOV)", 
            type=['mp4', 'avi', 'mov']
        )
        
        # Add text area for additional comments
        additional_comments = st.text_area(
            "Add any specific aspects you want analyzed:",
            placeholder="Example: Provide additional comments for Video Analytics",
        )

    if uploaded_file and api_key:
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                tmp_file.write(uploaded_file.read())
                video_path = tmp_file.name

            # Initialize analyzer
            analyzer = SoccerVideoAnalyzer(api_key)
            
            # Get video metadata
            metadata = analyzer.get_video_metadata(video_path)
            
            with col2:
                st.subheader("Video Information")
                st.write(f"Duration: {metadata['duration']:.2f} seconds")
                st.write(f"FPS: {metadata['fps']}")
                st.write(f"Resolution: {metadata['resolution']}")
            
            # Analysis section
            if st.button("Start Analysis", type="primary"):
                with st.spinner("Extracting frames from video..."):
                    frames = analyzer.extract_frames(video_path)
                    st.success(f"Extracted {len(frames)} frames for analysis")
                
                with st.spinner("Performing tactical analysis..."):
                    result = analyzer.analyze_game_sequence(
                        frames, 
                        additional_comments=additional_comments
                    )
                    
                if result["status"] == "success":
                    # Display results
                    st.subheader("Analysis Results")
                    
                    # Create tabs for different aspects of analysis
                    tabs = st.tabs([
                        "Video", 
                        "Tactical Analysis"
                    ])
                    
                    with tabs[0]:
                        st.video(video_path)
                    
                    with tabs[1]:
                        st.markdown(result["analysis"])
                        
                        # Add download button for analysis
                        st.download_button(
                            "Download Analysis",
                            result["analysis"],
                            file_name="soccer_analysis.txt",
                            mime="text/plain"
                        )
                else:
                    st.error(f"Analysis failed: {result['message']}")

            # Clean up
            os.unlink(video_path)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            
    else:
        if not api_key:
            st.warning("Please enter your OpenAI API key to proceed.")
        if not uploaded_file:
            st.info("Please upload a video file to begin analysis.")

if __name__ == "__main__":
    main()
