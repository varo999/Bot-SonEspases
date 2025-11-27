from Controlador import *
import os
import sys

CLAVE_API = os.getenv("Clave_Api_Gemini")
BOT_TOKEN = "8193853610:AAH-MrO2x7HAjXApp8RvL2IYPDTMZPtvOm8"


preguntas_listado=[#PLC_Annex_2024-225.pdf
"¿Cuál es el nombre del centro educativo y el curso académico al que se aplica el anexo del Proyecto Lingüístico que se detalla en el documento?"
"¿Cuáles son los tres idiomas principales utilizados para impartir los módulos en los ciclos formativos que se enumeran a lo largo del anexo?"
"¿Cuántas y cuáles son las Familias Profesionales que se detallan en el documento?"
"En el primer curso del CFGS. DESENVOLUPAMENT D'APLICACIONS MULTIPLATAFORMA, ¿cuáles son los dos módulos que se imparten en inglés y cuántas horas tiene asignadas cada uno?"
"Considerando los módulos de primer y segundo curso del CFGS. DESENVOLUPAMENT D'APLICACIONS MULTIPLATAFORMA, ¿cuál es el módulo que tiene la mayor carga horaria, con cuántas horas, y en qué idioma se imparte?"
#PLC BORJA MOLL  revisio 19_20.pdf
"¿En qué fechas fue aprobado el Proyecto Lingüístico por el Claustro y por el Consell Social del centro?"
"Según las encuestas realizadas durante el curso 2016/17, ¿cuál era la situación más preocupante que se encontró en los ciclos formativos respecto a la presencia del catalán, y qué porcentaje de uso del catalán en esos ciclos fue reportado por el profesorado?"
"¿Cuál es el principal objetivo que se propone el centro respecto a la competencia lingüística de su alumnado, y cómo define el documento la competencia lingüística?"
"¿A qué principio normativo se acogerá el centro para compensar la falta de uso de la lengua catalana por parte del alumnado, y qué justifica la aplicación de este principio?"
"¿Quiénes deben formar parte de la Comissió Lingüística y, específicamente, de cuántas horas de reducción horaria dispone el coordinador lingüístico para sus funciones?"
"En el primer curso del CFGS. COMERÇ INTERNACIONAL, ¿cuáles son los dos módulos que se imparten en castellano, y cuál es el módulo que se imparte en inglés con la mayor carga horaria?"
"En el segundo curso del CFGS. COMERÇ INTERNACIONAL, ¿en qué idioma se imparten los módulos de Comerç digital internacional y Negociació internacional, y cuál es la carga horaria total de estos dos módulos combinados?"
#PDC_2023.pdf
"¿En qué fechas fue aprobado el Pla Digital de Centre por el Claustre y el Consell Social, y a qué curso académico corresponde esta versión inicial del documento?"
"Según los datos básicos de infraestructura, ¿cuántos ordenadores portátiles y ordenadores de sobremesa tiene el centro, y cuántas pizarras interactivas se encuentran disponibles?"
"Al realizar el informe SELFIE (13/02/2023), ¿qué porcentaje de participación se registró para el equipo directivo, el profesorado y el alumnado, respectivamente?"
"Menciona dos de las principales fortalezas identificadas en el análisis DAFO del centro, referentes a la satisfacción y utilización de recursos tecnológicos por parte de los docentes y el alumnado."
"¿Cuáles son las tres dimensiones principales (pedagógica, organizativa o tecnológica) en las que se dividen las líneas estratégicas de actuación del Plan de Acción (PDC)?"
"En la Línea Estratégica 4 (Prácticas de Evaluación), ¿cuál es el objetivo específico (letra) que busca impulsar el sistema de rúbricas digitales, y cuáles son el valor de referencia y la meta (en porcentaje de profesorado) establecidos para este objetivo?"
"En la Línea Estratégica 1 (Liderazgo y Gobernanza), ¿cuál es el objetivo principal (letra) propuesto para digitalizar las tareas burocráticas del profesorado, y cuál es la meta (en porcentaje) establecida para la realización de las actas de reuniones por el Gestib?"
#Pla de convivència 2024-25.pdf
"¿En qué fechas fue aprobado el Pla de Convivència i Benestar por el Consell Social e informado al Claustre? Además, ¿cuál es la definición que ofrece el documento sobre este Plan?"
"El CIFP Francesc de Borja Moll está distribuido en tres edificios (A, B y C). ¿Cuántas plantas ocupa cada bloque? ¿Cuál es la capacidad aproximada del centro para el turno de mañana y para el turno de tarde, y a qué se debe la diferencia?"
"El Plan describe la diversidad del alumnado. ¿Qué características principales se mencionan para el perfil de los alumnos de los ciclos de Grau Bàsic de Informàtica y Perruqueria, especialmente en cuanto a edad y trayectoria escolar?"
"¿Cuál es el principal objetivo de la propuesta de estudio que se incluye en las Mesures de detecció para el curso 2024-25, y qué aspectos específicos se incluyen en este análisis?"
"¿Cómo está compuesto el personal no docente del centro (conserges, seguridad, técnicos, limpieza), y en qué turnos trabajan?"
"En la família professional de Sanitat, ¿cuál es el ciclo formativo que tiene el mayor número total de alumnos matriculados (hombres y mujeres combinados), y cuántos alumnos tiene en total?"
"En la família professional de Informàtica i Comunicacions, ¿cuál es el ciclo formativo con la mayor diferencia absoluta entre el número de hombres y mujeres, y cuál es esa diferencia?  (Indica el número de hombres y mujeres)."
#PGA 2024-25.pdf
"¿Qué órganos del centro (Claustre, Consell Social, Directora) aprobaron o fueron informados sobre la PGA 2024/2025 y sus componentes, y en qué fechas se realizaron estas aprobaciones/informes?"
"¿cuáles son los tres días no lectivos de libre disposición que fueron aprobados por el Claustre para el curso 2024/2025?"
"¿Cuál es el horario de apertura del centro (desde qué hora hasta qué hora), y cuál es la duración de una sesión de clase y del tiempo de recreo (esplai)?"
"Menciona una de las principales conclusiones globales positivas extraídas de la memoria del curso anterior (2023/2024) que se refleja en el Diagnóstico Inicial."
"¿En qué mes está previsto que se realice la evaluación final extraordinaria (recuperaciones) de los módulos de primer curso y la evaluación final de los módulos de segundo curso (excepto FCT/Projecte)?"
"De la familia profesional de Informàtica i Comunicacions, ¿cuál es el único Ciclo Formativo de Grado Medio (CFGM) que se ofrece en el turno de mañana, y qué grupo o modalidad imparte?"
"¿Cuántos Ciclos Formativos de Grado Superior (CFGS) y cuántos Ciclos Formativos de Grado Medio (CFGM) se ofrecen en la familia profesional de Sanitat en el turno de tarde, y cuál es el nombre completo de uno de los CFGS y uno de los CFGM ofrecidos en este turno?"
#NOFIC_2025.pdf
"¿Quién forma parte del Consell Social y cuántos membres té?"
"Quines són les funcions principals del Claustre de professorat?"
"¿Qué comisiones o coordinaciones docentes existen en el centro?"
"¿Cuáles son las normas generales para el uso de espacios e instalaciones del centro?"
"¿Qué derechos y deberes tiene el personal no docent?"
"¿Qué establece el documento respecto al dret de vaga de l’alumnat i del professorat?"
"¿Qué normas regula el uso de mòbils i dispositius electrònics dins del centre?"
"¿Cómo se estructura el pla de convivència segons el document?"
"¿Qué procedimientos existen para actuar en casos daccidents escolars o absències del professorat?"
]


if __name__ == "__main__":
    print("Iniciando Controlador......")
    
    controlador = None
    
    try:
        controlador = Controlador(
            api_key=CLAVE_API, 
            token=BOT_TOKEN
        )
        
    except KeyboardInterrupt:
        
        print("\nBot detenido. Iniciando proceso de limpieza...")
        if controlador: 
            controlador.limpiar_todo()
        
    except Exception as e:
        print(f"❌ Error fatal al iniciar el sistema: {e}")