import gradio as gr
import yt_dlp
import os

def download_audio(url):
    """
    Procesa el enlace proporcionado y extrae el audio en formato MP3.
    """
    if not url:
        return None, "Por favor, ingresa un enlace válido."
    
    # Nombre base para el archivo temporal
    output_base = "audio_descargado"
    
    # Configuración de yt-dlp optimizada para audio de alta calidad
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f"{output_base}.%(ext)s",
        'quiet': True,
        'no_warnings': True
    }

    try:
        # Limpieza de ejecuciones previas para evitar conflictos de archivos
        if os.path.exists(f"{output_base}.mp3"):
            os.remove(f"{output_base}.mp3")

        # Ejecución de la descarga y conversión
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Validación de la existencia del archivo generado
        if os.path.exists(f"{output_base}.mp3"):
            return f"{output_base}.mp3", "✅ ¡Proceso completado! El archivo está listo para descargar."
        else:
            return None, "❌ Error: El archivo no pudo ser generado por el servidor."
            
    except Exception as e:
        # Captura de errores técnicos (ej. enlaces caídos o problemas de red)
        return None, f"❌ Error técnico: {str(e)}"

# Diseño de la interfaz con Gradio Blocks
with gr.Blocks(title="Extractor de Audio", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📥 Extractor de Audio MP3")
    gr.Markdown("Extrae el audio de cualquier video de forma rápida y gratuita. Ideal para guardar música o podcasts en tu celular.")
    
    with gr.Group():
        with gr.Row():
            url_input = gr.Textbox(
                label="URL del Video", 
                placeholder="Pega aquí el link de YouTube, Vimeo, etc.",
                lines=1,
                scale=4
            )
        
        process_btn = gr.Button("🚀 OBTENER MP3", variant="primary")
    
    # Área de resultados
    with gr.Row():
        status_output = gr.Textbox(label="Estado", interactive=False)
    
    file_output = gr.File(label="Descargar Archivo")

    # Mapeo de la acción del botón
    process_btn.click(
        fn=download_audio,
        inputs=[url_input],
        outputs=[file_output, status_output]
    )

    gr.Markdown("---")
    gr.Markdown("💡 **Consejo:** Una vez que aparezca el archivo en el recuadro superior, presiona la flecha de descarga para guardarlo en tu dispositivo.")

# Punto de entrada de la aplicación
if __name__ == "__main__":
    demo.launch()
