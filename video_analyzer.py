import cv2
import base64
from openai import OpenAI
from typing import List
from PIL import Image
import io

class SoccerVideoAnalyzer:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.frame_interval = 30
    
    def extract_frames(self, video_path: str) -> List[str]:
        frames = []
        video = cv2.VideoCapture(video_path)
        frame_count = 0
        
        while video.isOpened():
            success, frame = video.read()
            if not success:
                break
                
            if frame_count % self.frame_interval == 0:
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convert to PIL Image
                pil_image = Image.fromarray(frame_rgb)
                # Resize image
                resized_image = self.resize_image(pil_image)
                # Convert to base64
                buffered = io.BytesIO()
                resized_image.save(buffered, format="JPEG")
                frame_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                frames.append(frame_base64)
            
            frame_count += 1
            
        video.release()
        return frames
    
    def analyze_game_sequence(self, frames: List[str] , additional_comments) -> dict:
        
        try:
            prompt = self.update_analysis_prompt_with_comments(additional_comments)
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ] + [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{frame}"
                            }
                        } for frame in frames
                    ]
                }
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=2000
            )
            
            return {
                "status": "success",
                "analysis": response.choices[0].message.content
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def get_video_metadata(self, video_path: str) -> dict:
        """Get basic video information"""
        video = cv2.VideoCapture(video_path)
        try:
            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(video.get(cv2.CAP_PROP_FPS))
            duration = total_frames / fps
            width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            return {
                "total_frames": total_frames,
                "fps": fps,
                "duration": duration,
                "resolution": f"{width}x{height}"
            }
        finally:
            video.release()
            
    def resize_image(self, image, max_short_dimension=768, max_long_dimension=2000):
        width, height = image.size
        if width > height:
            scaling_factor = min(max_long_dimension / width, max_short_dimension / height)
        else:
            scaling_factor = min(max_short_dimension / width, max_long_dimension / height)
        
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        return image.resize((new_width, new_height), Image.LANCZOS)
    
    
    def update_analysis_prompt_with_comments(self, comments):
        base_prompt = """As an expert soccer coach, analyze this match sequence and provide detailed tactical insights for Northwestern team's improvement. 
Focus on real game situations and practical recommendations: 

(Provide two sections: SHORT Higher level points and LONG FORM sections)

1. Play Situation Analysis:
   - What specific game situation is occurring? (e.g., corner kick, counter-attack, build-up play)
   - How are Northwestern players positioned?
   - What are the opponent's defensive/offensive arrangements?
   - Key player movements and their effectiveness
   - Critical decision-making moments

2. Tactical Execution Assessment:
   A. Offensive Organization:
      - Quality of attacking movement
      - Passing options created
      - Space utilization
      - Support player positioning
      - Timing of runs
      
   B. Defensive Structure:
      - Defensive line organization
      - Marking assignments
      - Pressing effectiveness
      - Recovery positions
      - Defensive transitions

3. Player Positioning Analysis:
   - Are players in optimal positions for this situation?
   - Gaps in defensive coverage
   - Attacking space creation
   - Supporting positions
   - Transition positioning

4. Immediate Tactical Improvements:
   Example format:
   - Current Issue: "Wide players dropping too deep during build-up"
   - Solution: "Maintain higher positioning to stretch defense"
   - Current Issue: "Slow defensive transition after set-piece"
   - Solution: "Designate specific recovery positions"

5. Team Movement Patterns:
   - Build-up play structure
   - Counter-attacking routes
   - Defensive shifting
   - Press triggers
   - Set-piece organization

6. Specific Coaching Points:
   A. Individual Instructions:
      - Player-specific positioning adjustments
      - Movement timing improvements
      - Decision-making guidance
      - Role-specific responsibilities

   B. Team Instructions:
      - Formation adjustments
      - Pressing triggers
      - Transition protocols
      - Set-piece organization

7. Game Situation Recommendations:
   For each identified situation, provide:
   - Current tactical approach
   - Recommended adjustments
   - Specific player instructions
   - Expected outcomes
   - Alternative strategies

8. Training Focus Areas:
   Based on observed patterns, suggest:
   - Specific drills to address issues
   - Game-situation replications
   - Position-specific exercises
   - Team coordination practices

Focus your analysis on:
- Real game situations visible in the sequence
- Practical, implementable improvements
- Clear tactical adjustments
- Specific player and team instructions

Provide recommendations that are:
- Immediately applicable in games
- Clear and specific to the situation
- Based on observed team patterns
- Focused on Northwestern's playing style

For each tactical point, explain:
- Why it needs improvement
- How to implement the change
- Expected impact on team performance
- Potential challenges in implementation

Remember to:
- Be specific to what's visible in the video
- Focus on practical, game-ready solutions
- Consider Northwestern's current playing style
- Provide clear, actionable coaching points."""
        
        if comments.strip():
            base_prompt += f"\n\nAdditional Analysis Focus:\n{comments}"
            
        return base_prompt