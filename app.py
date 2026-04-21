import streamlit as st
import yt_dlp
import os

# Configuración de la interfaz para dispositivos móviles
st.set_page_config(page_title="Extractor de MP3", page_icon="📥", layout="centered")

st.title("📥 Extractor de Audio MP3")
st.markdown("Pega el enlace de un video para obtener el audio en alta calidad.")

# Entrada de URL
url = st.text_input("Enlace del video:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Procesar Descarga", use_container_width=True):
    if not url:
        st.warning("Por favor, ingresa un enlace.")
    else:
        with st.spinner("Descargando y convirtiendo..."):
            output_file = "audio_resultado"
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': f"{output_file}.%(ext)s",
                'quiet': True
            }

            try:
                # Eliminar archivos temporales previos si existen
                if os.path.exists(f"{output_file}.mp3"):
                    os.remove(f"{output_file}.mp3")

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                if os.path.exists(f"{output_file}.mp3"):
                    with open(f"{output_file}.mp3", "rb") as f:
                        st.download_button(
                            label="✅ Descargar MP3",
                            data=f,
                            file_name="audio_extraido.mp3",
                            mime="audio/mpeg",
                            use_container_width=True
                        )
                    st.success("¡Audio listo para descargar!")
                else:
                    st.error("Error al generar el archivo.")
            except Exception as e:
                st.error(f"Error en el proceso: {e}")

st.divider()
st.caption("Herramienta optimizada para uso móvil.")
