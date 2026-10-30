import collections 
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_advanced_pitch_deck():
    prs = Presentation()
    
    # 16:9 Aspect Ratio (Widescreen)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette (Cyberpunk / Tech Theme)
    bg_dark = RGBColor(11, 15, 25)       # Deepest blue/black
    panel_bg = RGBColor(30, 41, 59)      # Slate 800 (for cards)
    accent_blue = RGBColor(56, 189, 248) # Cyan/Sky blue
    accent_pink = RGBColor(236, 72, 153) # Neon pink
    text_white = RGBColor(248, 250, 252) # Off white
    text_gray = RGBColor(148, 163, 184)  # Slate 400
    
    color_safe = RGBColor(34, 197, 94)   # Green
    color_warn = RGBColor(234, 179, 8)   # Yellow
    color_danger = RGBColor(239, 68, 68) # Red

    def set_background(slide):
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = bg_dark
        
        # Add a top accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.15))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent_blue
        bar.line.color.rgb = accent_blue

    # --- Slide 1: TITLE SLIDE ---
    slide1 = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
    set_background(slide1)
    
    # Add Smartphone Image to Title Slide
    try:
        slide1.shapes.add_picture(r"C:\Users\Asus\.gemini\CodeShield\brain\c2400b79-0374-4c97-9c61-dd2edaee9084\iqoo_phone_ai_1788684855575.jpg", Inches(0), Inches(0), width=Inches(13.33))
    except Exception as e:
        print("Could not load image 1:", e)
        
    # Semi-transparent overlay to make text readable
    overlay = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    overlay.fill.solid()
    overlay.fill.fore_color.rgb = bg_dark
    # Python-pptx doesn't natively do transparency easily via simple API, but we'll place the text cards on top.
    
    # Center Card
    card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(2), Inches(10.33), Inches(3.5))
    card.fill.solid()
    card.fill.fore_color.rgb = panel_bg
    card.line.color.rgb = accent_blue
    card.line.width = Pt(2)
    
    # Title Text
    tx_box = slide1.shapes.add_textbox(Inches(2), Inches(2.2), Inches(9.33), Inches(1.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.add_paragraph()
    p.text = "CodeShield"
    p.font.bold = True
    p.font.size = Pt(72)
    p.font.color.rgb = accent_blue
    p.font.name = 'Century Gothic'
    p.alignment = PP_ALIGN.CENTER
    
    p2 = tf.add_paragraph()
    p2.text = "The Phone-First Firewall for AI Agents"
    p2.font.bold = True
    p2.font.size = Pt(36)
    p2.font.color.rgb = text_white
    p2.font.name = 'Century Gothic'
    p2.alignment = PP_ALIGN.CENTER

    # Subtitle
    tx_box2 = slide1.shapes.add_textbox(Inches(2), Inches(4.2), Inches(9.33), Inches(1))
    tf2 = tx_box2.text_frame
    p3 = tf2.add_paragraph()
    p3.text = "Track 06: Developer Tools  |  iQOO Hackathon 2026"
    p3.font.size = Pt(20)
    p3.font.color.rgb = accent_pink
    p3.alignment = PP_ALIGN.CENTER

    # --- Helper for standard slides ---
    def create_standard_slide(title, subtitle):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        set_background(slide)
        
        # Title
        t_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(12), Inches(1))
        tp = t_box.text_frame.add_paragraph()
        tp.text = title
        tp.font.bold = True
        tp.font.size = Pt(44)
        tp.font.color.rgb = accent_blue
        tp.font.name = 'Century Gothic'
        
        # Subtitle
        sp = t_box.text_frame.add_paragraph()
        sp.text = subtitle
        sp.font.size = Pt(20)
        sp.font.color.rgb = text_gray
        sp.font.name = 'Century Gothic'
        
        return slide

    def add_card(slide, x, y, w, h, title, body_lines, accent_rgb):
        # Background shape
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        shape.fill.solid()
        shape.fill.fore_color.rgb = panel_bg
        shape.line.color.rgb = accent_rgb
        shape.line.width = Pt(1.5)
        
        # Text
        tx = slide.shapes.add_textbox(Inches(x+0.2), Inches(y+0.2), Inches(w-0.4), Inches(h-0.4))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p = tf.add_paragraph()
        p.text = title
        p.font.bold = True
        p.font.size = Pt(24)
        p.font.color.rgb = accent_rgb
        
        for line in body_lines:
            bp = tf.add_paragraph()
            bp.text = line
            bp.font.size = Pt(18)
            bp.font.color.rgb = text_white
            bp.space_before = Pt(10)

    # --- Slide 2: The Problem (Split Layout) ---
    s2 = create_standard_slide("The Problem", "Autonomous AI coding agents are dangerous without boundaries.")
    add_card(s2, 1, 2, 5, 4.5, "Context Blindness", ["Feeding an entire 2,000-line file to an AI to review a 3-line change overwhelms the model, leading to hallucinations and bad code generation."], accent_pink)
    add_card(s2, 7, 2, 5, 4.5, "Unsafe Execution", ["Allowing autonomous agents to execute shell commands directly on a host machine is extremely dangerous.", "Example: Executing 'rm -rf' or dropping a production database by mistake."], color_danger)

    # --- Slide 3: The Solution ---
    s3 = create_standard_slide("The Solution", "Edge-Native Zero-Trust Execution")
    
    try:
        s3.shapes.add_picture(r"C:\Users\Asus\.gemini\CodeShield\brain\c2400b79-0374-4c97-9c61-dd2edaee9084\cyber_firewall_1788684911557.jpg", Inches(0), Inches(2), width=Inches(13.33))
    except Exception as e:
        print("Could not load image 2:", e)
        
    add_card(s3, 1, 2.5, 11, 4.0, "CodeShield: The Execution Firewall", 
             ["• We decoupled the generation from the execution.",
              "• We built a firewall that grades AI intents into 3 Risk Tiers before they ever touch the terminal.",
              "• Instead of relying on the cloud, CodeShield places the security evaluation natively on the iQOO smartphone.",
              "• This creates absolute privacy, zero-latency, and an unhackable hardware security key."], accent_blue)

    # --- Slide 4: Phone-First Architecture ---
    s4 = create_standard_slide("Phone-First Architecture", "Orchestrating the Laptop and the iQOO device.")
    add_card(s4, 0.5, 2, 3.8, 4, "1. The Laptop (Green Light)", ["The developer works on the laptop.", "When AI proposes code execution, the local terminal pauses and intercepts the command."], text_white)
    add_card(s4, 4.7, 2, 3.8, 4, "2. Office Kit Bridge", ["The proposed command and the relevant code slice are beamed seamlessly to the iQOO device via iQOO Office Kit."], accent_pink)
    add_card(s4, 8.9, 2, 3.8, 4, "3. Snapdragon NPU", ["The iQOO phone acts as the physical security brain.", "A local open-source LLM evaluates the threat level completely offline."], accent_blue)

    # --- Slide 5: The 3 Risk Tiers ---
    s5 = create_standard_slide("Creative Phone Use for Security", "Dynamic Threat Mitigation Pipeline")
    add_card(s5, 1, 2, 3.5, 4, "TIER 1 (SAFE)", ["Read-only commands (e.g., 'echo', 'ls').", "Executed automatically inside the Docker sandbox.", "Zero friction."], color_safe)
    add_card(s5, 4.8, 2, 3.5, 4, "TIER 2 (WRITE)", ["Non-destructive writes (e.g., 'touch').", "Executed in an isolated Docker container to prevent host contamination."], color_warn)
    add_card(s5, 8.6, 2, 3.5, 4, "TIER 3 (DESTRUCTIVE)", ["High-risk (e.g., 'rm -rf').", "HARD-BLOCKED.", "Triggers physical alert on iQOO screen.", "Requires VOICE APPROVAL into the phone microphone to unlock."], color_danger)

    # --- Slide 6: Technical Depth ---
    s6 = create_standard_slide("Deep Technical Infrastructure", "Built for the Edge.")
    add_card(s6, 1, 1.8, 11, 1.2, "AST Slicing (Tree-Sitter)", ["Surgical Abstract Syntax Tree code extraction to save NPU memory."], accent_blue)
    add_card(s6, 1, 3.2, 11, 1.2, "Local RAG (ChromaDB / SQLite)", ["Semantic indexing system for offline project memory."], accent_pink)
    add_card(s6, 1, 4.6, 11, 1.2, "Sandbox Executor (Docker)", ["Ephemeral containers ensure malicious code never touches the host."], color_safe)
    add_card(s6, 1, 6.0, 11, 1.2, "CI/CD Webhook (FastAPI)", ["Automated server to intercept GitHub Pull Requests."], color_warn)

    # --- Slide 7: Conclusion ---
    s7 = create_standard_slide("Why CodeShield Wins", "Protecting the Future of Enterprise AI")
    add_card(s7, 1.5, 2, 10, 4.5, "Ready for the 30-Hour Battle.", 
             ["✓ 100% Offline & Private (Protects enterprise IP)", 
              "✓ Deep utilization of Snapdragon NPU & Office Kit",
              "✓ Fully functioning 11-commit prototype repository ready to demo.",
              "",
              "Thank you."], accent_blue)

    prs.save('CodeShield_Hackathon_Pitch_V3.pptx')
    print("Successfully generated CodeShield_Hackathon_Pitch_V3.pptx")

if __name__ == '__main__':
    create_advanced_pitch_deck()

