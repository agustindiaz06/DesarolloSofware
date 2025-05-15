from newspaper import Article
import sys

def extraer_articulo(url):
    try:
        articulo = Article(url, language='es')
        articulo.download()
        articulo.parse()  # NO se llama a .nlp(), así no requiere punkt

        resultado = {
            'titulo': articulo.title or 'No disponible',
            'autores': ', '.join(articulo.authors) if articulo.authors else 'No disponible',
            'fecha': articulo.publish_date.strftime('%Y-%m-%d') if articulo.publish_date else 'No disponible',
            'contenido': articulo.text.strip()
        }

        return resultado

    except Exception as e:
        return {'error': f'Error al procesar la URL: {str(e)}'}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python extractor.py <URL-del-articulo>")
        sys.exit(1)

    url = sys.argv[1]
    resultado = extraer_articulo(url)

    if 'error' in resultado:
        print(resultado['error'])
    else:
        print(f"Título: {resultado['titulo']}")
        print(f"Autor(es): {resultado['autores']}")
        print(f"Fecha: {resultado['fecha']}")
        print("\nContenido:\n")
        print(resultado['contenido'][:1000] + '...')  # Muestra resumen si el texto es largo


        