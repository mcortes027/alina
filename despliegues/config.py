# Este archivo contempla los distintos entornos en los que permitimos despliegues, para añadir un nuevlo entorno copie la templeta.
# Y edítela según necesite. 

# ENTORNO PARA DESPLIEGUE EN CLASE. 
#"volumen_mysql":r'C:\Users\JRBlanco\Dev\reto_server\mysql_data'


entornos ={
      'angela':{
            "volumen_chromadb":'C:\\Users\\PC\\Dev\\alina\\chromadb-data',
            "volumen_ollama":'C:\\Users\\PC\\Dev\\alina\\ollama-data',
            "volumen_mysql":'C:\\Users\\PC\\Dev\\alina\\mysql_data',
            "volumen_backups":'C:\\Users\\PC\\Dev\\alina\\backups',
            "volumen_code":'C:\\alina\\app',
            "volumen_audio":'C:\\Users\\PC\\Dev\\alina\\audio'
      },
      'manolo':{
            "volumen_chromadb":'C:\\Users\\m_cor\\Dev\\alina\\chromadb-data',
            "volumen_ollama":'C:\\Users\\m_cor\\Dev\\alina\\ollama-data',
            "volumen_mysql":'C:\\Users\\m_cor\\Dev\\alina\\mysql_data',
            "volumen_backups":'C:\\Users\\m_cor\\Dev\\alina\\backups',
            "volumen_code":'C:\\Users\\m_cor\Dev\\alina\\alina\\app',
            "volumen_audio":'C:\\Users\\m_cor\\Dev\\alina\\audio'
            
      }         
} 


