import base64
from google.genai import types
from openai import OpenAI
from google.adk.tools.tool_context import ToolContext

client = OpenAI()

async def generate_images(tool_context: ToolContext):
     prompt_builder_ouput = tool_context.state.get("prompt_builder_ouput")
     optimized_prompts = prompt_builder_ouput.get("optimized_prompts")

     generated_images = []

     existing_artifacts = await tool_context.list_artifacts()

     for prompt in optimized_prompts:
        scene_id = prompt.get("scene_id")
        enhanced_prompt = prompt.get("enhanced_prompt")
        filename = f"scene_{scene_id}_image.jpeg"

        # 이미지가 있는 지 확인하여 더 이상 생성시키지 않음
        if filename in existing_artifacts:
            generated_images.append({
                "scene_id": scene_id,
                "prompt": enhanced_prompt[:100],
                "filename": filename,
            })
            continue

        image = client.images.generate(
            model="gpt-image-1",
            prompt=enhanced_prompt,
            quality='low',
            n=1,
            moderation='low',
            output_format='jpeg',
            background='opaque',
            size="1024x1536",
        )

        image_bytes = base64.b64decode(image.data[0].b64_json)
        
        artifact = types.Part(
            inline_data=types.Blob(
                mime_type="image/jpeg",
                data=image_bytes,
            )
        )
        
        await tool_context.save_artifact(
            filename=filename, 
            artifact=artifact,
        )

        generated_images.append({
            "scene_id": scene_id,
            "prompt": enhanced_prompt[:100],
            "filename": filename,
        })

        return {
            "total_images": len(generated_images),
            "generated_images": generated_images,
            "status": "complete"
        }
