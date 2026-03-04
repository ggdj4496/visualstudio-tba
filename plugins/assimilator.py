import cv2

def procesar_asimilacion(frame, capa_bot):
    # En lugar de superponer, mezclamos con transparencia fija
    # para evitar que se dupliquen los rasgos faciales
    if frame is None or capa_bot is None:
        return frame
        
    # Redimensionar capa al tamaño del frame
    capa_res = cv2.resize(capa_bot, (frame.shape[1], frame.shape[0]))
    
    # Mezcla balanceada: 50% humano, 50% bot
    resultado = cv2.addWeighted(frame, 0.5, capa_res, 0.5, 0)
    return resultado