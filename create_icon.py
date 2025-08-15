# Python script to generate a simple icon
# Requires Pillow library: pip install Pillow

try:
    from PIL import Image, ImageDraw
    
    # Create a 32x32 icon
    image = Image.new('RGB', (32, 32), color=(73, 109, 137))
    draw = ImageDraw.Draw(image)
    
    # Draw a simple shape as the icon
    draw.rectangle([8, 8, 24, 24], fill=(255, 255, 255))
    draw.rectangle([12, 12, 20, 20], fill=(73, 109, 137))
    
    # Save as ICO file
    image.save('app_icon.ico')
    
    print("Icon created: app_icon.ico")
except ImportError:
    print("Error: Pillow library not installed, please run 'pip install Pillow'")
    exit(1)
except Exception as e:
    print(f"Error creating icon: {e}")
    exit(1)