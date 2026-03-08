[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md) | [Français](README_FR.md) | [Español](README_ES.md)

# Feed de inteligencia de amenazas de honeypot HFish

[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/yuexuan521/honeypot-blocklist)
[![Source](https://img.shields.io/badge/Source-HFish-blue.svg)](https://hfish.net/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)
[![Data Quality Check](https://github.com/yuexuan521/honeypot-blocklist/actions/workflows/data_quality.yml/badge.svg)](https://github.com/yuexuan521/honeypot-blocklist/actions/workflows/data_quality.yml)
[![Release](https://img.shields.io/github/v/release/yuexuan521/honeypot-blocklist)](https://github.com/yuexuan521/honeypot-blocklist/releases)

Feed de direcciones IP maliciosas de alta confianza, generado automáticamente a partir de la **telemetría de honeypots HFish**, diseñado para entornos de **firewall / WAF / SIEM / IPSet / EDL**.

Este proyecto recopila continuamente las IP de origen observadas por honeypots HFish expuestos a Internet, aplica filtrado automático y listas blancas, y publica un feed limpio y fácil de integrar en sistemas defensivos y flujos de automatización.

> **Advertencia**
> Este feed se genera automáticamente. Aunque se aplican filtrado y listas blancas, se recomienda evaluar su impacto en tu propio entorno antes de usarlo en producción.

---

## Por qué existe este proyecto

Los honeypots expuestos a Internet reciben de forma constante intentos de fuerza bruta, escaneos de vulnerabilidades, pruebas de credenciales débiles y otro tráfico de ataque automatizado.  
El objetivo de este repositorio es convertir esas observaciones reales en un **feed de inteligencia defensiva** reutilizable para ayudar a los usuarios a:

- bloquear rápidamente IP maliciosas recientes en el perímetro de red
- enriquecer detecciones de SIEM / SOAR con una señal adicional de amenaza
- generar automáticamente reglas de bloqueo para firewalls Linux, servicios web y entornos edge
- construir su propio feed privado de inteligencia de amenazas basado en HFish

---

## Características principales

- **Feed continuo de IP maliciosas de las últimas 24 horas**
- **Actualización automática cada 2 a 4 horas**
- **URL de suscripción en texto plano**
- **SDK de Python y CLI incluidos**
- **Compatibilidad con Docker**
- **Ejemplos de integración para Nginx, Linux Firewall, Cloudflare y Palo Alto**
- **Proyecto open source bajo licencia MIT**

---

## URL del feed

Puedes integrar directamente la siguiente URL en tus dispositivos de seguridad, scripts o flujos automatizados:

| Formato | URL | Caso de uso |
|---|---|---|
| TXT | `https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt` | EDL de firewall, Linux IPSet, WAF, enriquecimiento de SIEM |

---

## Perfil del feed

| Elemento | Valor |
|---|---|
| Fuente de datos | HFish Honeypot (V3+) |
| Alcance de observación | Internet público |
| Actividad incluida | fuerza bruta SSH/RDP, escaneo web / explotación de vulnerabilidades, sondeo de servicios no autorizados |
| Ventana temporal | últimas 24 horas |
| Frecuencia de actualización | cada 2 a 4 horas |
| Procesamiento de datos | limpieza automática y filtrado básico mediante lista blanca |
| Exclusiones comunes | GoogleBot, BingBot, servicios de GitHub, Cloudflare y otras infraestructuras legítimas conocidas cuando aplique |

---

## Por qué este feed es confiable

Este proyecto está diseñado para ser **simple, transparente, auditable y fácil de automatizar**.

- **Formato de datos abierto**: una IP por línea, fácil de revisar, analizar e integrar
- **Cadena de herramientas abierta**: la lógica de generación, el cliente y la CLI están disponibles públicamente en el repositorio
- **Límites claramente documentados**: la posibilidad de falsos positivos se indica explícitamente
- **Orientado al uso real**: pensado para entornos defensivos reales, no solo como demostración

Aun así, ningún feed automatizado de inteligencia de amenazas es perfecto.  
Salidas de red compartidas, NAT, hosts comprometidos o reasignación dinámica de IP pueden introducir ruido o falsos positivos. En producción, se recomienda observar y probar antes de aplicar bloqueos estrictos.

---

## Casos de uso recomendados

Este feed es adecuado para:

- bloquear rápidamente IP maliciosas conocidas en el perímetro de red
- alimentar una **EDL (External Dynamic List)** en firewalls empresariales
- enriquecer plataformas **SIEM / SOAR**
- generar automáticamente reglas de **Linux IPSet / iptables**
- producir reglas de denegación para **Nginx**
- implementar lógica ligera de bloqueo en **Cloudflare Workers** u otros entornos edge

---

## Inicio rápido

### Linux IPSet + iptables

```bash
# 1) Descargar el feed más reciente
wget -O /tmp/blacklist.txt https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt

# 2) Crear un conjunto IPSet
ipset create honeypot_blacklist hash:ip hashsize 4096

# 3) Importar las IP
while read ip; do
  ipset add honeypot_blacklist "$ip"
done < /tmp/blacklist.txt

# 4) Bloquear el tráfico coincidente
iptables -I INPUT -m set --match-set honeypot_blacklist src -j DROP
```

------

## Uso para desarrolladores

### SDK de Python

```python
from tools.client import ThreatFeedClient

feed = ThreatFeedClient()
feed.fetch_data()

if feed.is_malicious("1.2.3.4"):
    print("Esta IP debería bloquearse")
else:
    print("Esta IP no está actualmente en el feed")
```

### CLI

```bash
# Actualizar los datos locales
python3 tools/cli.py --update

# Verificar si una IP está en el feed
python3 tools/cli.py --check 1.2.3.4

# Exportar como JSON
python3 tools/cli.py --export json

# Exportar como TXT
python3 tools/cli.py --export txt
```

### Docker

```bash
docker build -t hfish-feed .
docker run --rm hfish-feed --check 1.1.1.1
```

------

## Ejemplos de integración

El directorio `integrations/` contiene ejemplos listos para usar para varias plataformas:

| Plataforma     | Tipo          | Uso                                                    |
| -------------- | ------------- | ------------------------------------------------------ |
| Nginx          | Script        | Generación de reglas de denegación para servidores web |
| Linux Firewall | Script        | Bloqueo eficiente con `ipset` + `iptables`             |
| Cloudflare     | Worker        | Lógica de bloqueo en el edge                           |
| Palo Alto      | Documentación | Integración con External Dynamic List (EDL)            |

------

## Construye tu propio feed de HFish

Si operas tu propio entorno HFish, puedes reutilizar las herramientas de este proyecto para generar un feed privado o específico para tu organización.

Herramientas relevantes:

- `tools/generate_feed.py`
- `tools/update_feed.sh`

Artículo de referencia:

- **Guía práctica para construir una fuente automatizada de inteligencia de amenazas con HFish + Python + GitHub Pages**

------

## Estructura del repositorio

```text
.
├── .github/workflows/       # comprobación de calidad de datos y automatización
├── integrations/            # ejemplos de integración por plataforma
├── tools/                   # generador, SDK cliente, CLI, scripts de actualización
├── tests/                   # pruebas
├── ip_list.txt              # feed publicado
└── README*.md               # documentación multilingüe
```

------

## Nivel de madurez del proyecto

Este proyecto se mantiene como una utilidad de seguridad pensada para escenarios defensivos reales, y no solo como una demostración.

Señales actuales de madurez del proyecto:

- repositorio público
- licencia open source clara
- documentación clara sobre la semántica del feed
- métodos de acceso mediante CLI y SDK
- ejemplos de integración
- workflow automatizado de control de calidad de datos

Antes de adoptarlo en producción, se recomienda evaluar:

- el alcance del bloqueo
- el manejo de falsos positivos
- las expectativas sobre la frecuencia de actualización
- la estrategia de reversión
- la necesidad de una lista blanca local

------

## Reporte de falsos positivos

Los falsos positivos no pueden eliminarse por completo.

Si crees que una IP fue incluida por error en el feed, abre una Issue e incluye, en la medida de lo posible:

- la dirección IP afectada
- el motivo de la reclamación
- evidencia de respaldo
- una marca de tiempo aproximada si está disponible

Esta información ayuda a mejorar la calidad del feed con el tiempo.

------

## Seguridad

Este repositorio publica un feed de inteligencia de amenazas y herramientas de apoyo.
**No constituye una solución de prevención completa ni debe utilizarse como único criterio de bloqueo.**

Buenas prácticas recomendadas:

- usarlo como una señal entre varias
- combinarlo con listas blancas locales
- probarlo primero en modo observación o en un alcance limitado
- tener precaución con rangos IP compartidos o dinámicos

Si descubres un problema de seguridad relacionado con el código del repositorio, la automatización o los scripts de integración, puedes usar primero GitHub Issues. Para temas sensibles, también puede habilitarse un canal privado.

------

## Contribuciones

Las contribuciones en código, documentación e ideas de mejora son bienvenidas.

Áreas útiles de contribución:

- mejora de la calidad del feed
- reducción de falsos positivos
- mejoras en el parser, el cliente o la CLI
- incorporación de nuevas integraciones
- correcciones de documentación y traducciones
- mejora de pruebas y CI

Para cambios importantes, se recomienda abrir primero una Issue para discutir el alcance y el enfoque antes de enviar un Pull Request.

------

## Hoja de ruta

Posibles líneas de mejora futuras:

- formatos de feed con metadatos más ricos
- supresión más estricta de falsos positivos
- más integraciones para firewalls / SIEM
- mayor cobertura de pruebas
- incorporación de estadísticas e información de transparencia

------

## Descargo de responsabilidad

1. **Precisión**
   Los datos se recopilan y procesan automáticamente. Intentamos reducir el ruido, pero hosts comprometidos, infraestructuras compartidas o IP dinámicas aún pueden aparecer en el feed.
2. **Uso bajo tu propia responsabilidad**
   Eres responsable de evaluar si este feed es adecuado para tu entorno antes de usarlo en producción.
3. **Limitación de responsabilidad**
   El mantenedor no será responsable de interrupciones del servicio, pérdida de conectividad, impacto operativo o pérdida de datos causados por el uso de este feed.

------

## Licencia

Este proyecto se publica bajo **MIT License**.

------

Impulsado por [HFish](https://hfish.net/) y automatización en Python.
