"""
Utilidades para sanitizar HTML del editor
"""
import bleach

# Tags HTML permitidos
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 's', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'a', 'blockquote', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'code', 'pre', 'hr', 'div', 'span'
]

# Atributos permitidos por tag
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target'],
    'table': ['border', 'cellpadding', 'cellspacing'],
    'th': ['colspan', 'rowspan'],
    'td': ['colspan', 'rowspan'],
    '*': ['class']  # Permitir class en todos los tags
}

# Estilos permitidos
ALLOWED_STYLES = []

def sanitize_html(content):
    """
    Sanitizar contenido HTML del editor para prevenir XSS
    
    Args:
        content (str): Contenido HTML a sanitizar
        
    Returns:
        str: Contenido HTML limpio y seguro
    """
    if not content:
        return ''
    
    # Limpiar HTML
    clean_content = bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        styles=ALLOWED_STYLES,
        strip=True  # Eliminar tags no permitidos en lugar de escaparlos
    )
    
    # Linkify URLs (convertir URLs en enlaces)
    clean_content = bleach.linkify(
        clean_content,
        parse_email=False  # No convertir emails en enlaces
    )
    
    return clean_content
