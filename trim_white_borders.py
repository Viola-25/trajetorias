import os
from PIL import Image, ImageChops

# Diretórios de origem e destino
DIRETORIO_ORIGEM = '.' # '.' significa a pasta atual
DIRETORIO_DESTINO = './cortadas'

def remover_bordas_verticais(caminho_imagem, caminho_destino):
    try:
        # Abre a imagem
        img = Image.open(caminho_imagem)
        
        # Converte para RGB temporariamente apenas para calcular a diferença 
        # (isso evita problemas caso a imagem PNG tenha canal de transparência Alpha)
        img_rgb = img.convert("RGB")
        
        # Cria um fundo 100% branco do mesmo tamanho
        fundo_branco = Image.new("RGB", img_rgb.size, (255, 255, 255))
        
        # Encontra a diferença entre a imagem original e o fundo branco
        diferenca = ImageChops.difference(img_rgb, fundo_branco)
        
        # getbbox() acha a "caixa delimitadora" do conteúdo que NÃO é branco
        # Retorna uma tupla: (esquerda, superior, direita, inferior)
        bbox = diferenca.getbbox()
        
        if bbox:
            # Como você quer tirar apenas as bordas superior e inferior,
            # forçamos a esquerda (0) e a direita (largura total) a se manterem iguais.
            bbox_vertical = (0, bbox[1], img.width, bbox[3])
            
            # Corta a imagem original usando as coordenadas calculadas
            img_cortada = img.crop(bbox_vertical)
            
            # Salva na nova pasta
            img_cortada.save(caminho_destino)
            print(f"✅ Cortada e salva: {os.path.basename(caminho_destino)}")
        else:
            print(f"⚠️ Imagem totalmente branca ignorada: {os.path.basename(caminho_imagem)}")
            
    except Exception as e:
        print(f"❌ Erro ao processar {os.path.basename(caminho_imagem)}: {e}")

def main():
    # Cria a pasta destino se ela não existir
    if not os.path.exists(DIRETORIO_DESTINO):
        os.makedirs(DIRETORIO_DESTINO)
        
    # Lista todos os arquivos .png da pasta atual (ignorando outras coisas)
    arquivos = [f for f in os.listdir(DIRETORIO_ORIGEM) if f.lower().endswith('.png')]
    
    if not arquivos:
        print("Nenhuma imagem .png encontrada neste diretório.")
        return

    print(f"🔍 Encontradas {len(arquivos)} imagens. Iniciando o corte...")
    
    # Processa cada imagem encontrada
    for arquivo in arquivos:
        caminho_completo = os.path.join(DIRETORIO_ORIGEM, arquivo)
        caminho_destino = os.path.join(DIRETORIO_DESTINO, arquivo)
        remover_bordas_verticais(caminho_completo, caminho_destino)
        
    print("🎉 Processo finalizado! Suas imagens estão na pasta 'cortadas'.")

if __name__ == '__main__':
    main()