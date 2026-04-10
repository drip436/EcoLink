"""
ecolink/pages/map_page.py
Mapa en tiempo real con Leaflet via iframe autónomo.
"""

import reflex as rx
import base64
from ecolink.state import State
from ecolink.components.ui import (
    navbar, notification_bar,
    C_GREEN_MID, C_ACCENT, C_BG, C_WHITE,
    C_GREEN_PALE, C_TEXT, C_MUTED,
)

# ── HTML completo del mapa (corre dentro de un iframe, sin conflictos con React) ──
_MAP_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>html,body,#map{margin:0;padding:0;width:100%;height:100%;}</style>
</head>
<body>
<div id="map"></div>
<script>
var map = L.map('map').setView([20.9674, -89.5926], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
    attribution:'&copy; OpenStreetMap contributors', maxZoom:18
}).addTo(map);

var ZONE_WP = {
    'Centro Norte': [{lat:20.9674,lng:-89.5926},{lat:20.9695,lng:-89.5940},{lat:20.9712,lng:-89.5955},{lat:20.9730,lng:-89.5965},{lat:20.9748,lng:-89.5950},{lat:20.9760,lng:-89.5932},{lat:20.9745,lng:-89.5910},{lat:20.9720,lng:-89.5900}],
    'Col. Sur':     [{lat:20.9520,lng:-89.5890},{lat:20.9505,lng:-89.5910},{lat:20.9488,lng:-89.5930},{lat:20.9470,lng:-89.5945},{lat:20.9455,lng:-89.5960},{lat:20.9440,lng:-89.5975},{lat:20.9460,lng:-89.5995},{lat:20.9480,lng:-89.5980}],
    'Zona Industrial':[{lat:20.9800,lng:-89.5600},{lat:20.9820,lng:-89.5580},{lat:20.9840,lng:-89.5560},{lat:20.9860,lng:-89.5545},{lat:20.9880,lng:-89.5530},{lat:20.9870,lng:-89.5510},{lat:20.9850,lng:-89.5525}],
    'Frac. Bello':  [{lat:20.9900,lng:-89.6100},{lat:20.9920,lng:-89.6120},{lat:20.9940,lng:-89.6140},{lat:20.9955,lng:-89.6160},{lat:20.9940,lng:-89.6180},{lat:20.9920,lng:-89.6170},{lat:20.9905,lng:-89.6150}],
    'Altabrisa':    [{lat:21.0010,lng:-89.6140},{lat:21.0030,lng:-89.6155},{lat:21.0050,lng:-89.6170},{lat:21.0065,lng:-89.6185},{lat:21.0055,lng:-89.6200},{lat:21.0035,lng:-89.6190},{lat:21.0015,lng:-89.6175}],
    'Garcia Gineres':[{lat:20.9760,lng:-89.6100},{lat:20.9775,lng:-89.6115},{lat:20.9790,lng:-89.6130},{lat:20.9805,lng:-89.6120},{lat:20.9815,lng:-89.6105},{lat:20.9800,lng:-89.6090},{lat:20.9780,lng:-89.6085}],
    'Itzimna':      [{lat:20.9850,lng:-89.6200},{lat:20.9865,lng:-89.6215},{lat:20.9880,lng:-89.6230},{lat:20.9895,lng:-89.6220},{lat:20.9885,lng:-89.6200},{lat:20.9870,lng:-89.6185}],
    'Uman':         [{lat:20.8900,lng:-89.7520},{lat:20.8920,lng:-89.7540},{lat:20.8940,lng:-89.7555},{lat:20.8960,lng:-89.7570},{lat:20.8945,lng:-89.7590},{lat:20.8925,lng:-89.7580}]
};

var STATUS_COLOR = {'in_progress':'#ff6d00','scheduled':'#1565c0','completed':'#2e7d32','cancelled':'#b71c1c'};
var layers = {};

var truckIcon = L.divIcon({html:'<div style="font-size:22px">&#x1F69B;</div>',className:'',iconSize:[28,28],iconAnchor:[14,14]});
var startIcon = L.divIcon({html:'<div style="font-size:18px">&#x1F4CD;</div>',className:'',iconSize:[22,22],iconAnchor:[11,22]});
var endIcon   = L.divIcon({html:'<div style="font-size:18px">&#x1F3C1;</div>',className:'',iconSize:[22,22],iconAnchor:[11,22]});

function normalize(s){
    return (s||'').toLowerCase()
        .replace(/\u00e1/g,'a').replace(/\u00e9/g,'e').replace(/\u00ed/g,'i')
        .replace(/\u00f3/g,'o').replace(/\u00fa/g,'u');
}
function getWP(zone){
    if(!zone) return ZONE_WP['Centro Norte'];
    if(ZONE_WP[zone]) return ZONE_WP[zone];
    var n=normalize(zone);
    for(var k in ZONE_WP){ if(normalize(k)===n) return ZONE_WP[k]; }
    return ZONE_WP['Centro Norte'];
}

function drawRoutes(routes){
    for(var id in layers){ layers[id].forEach(function(l){map.removeLayer(l);}); }
    layers={};
    var bounds=[];
    routes.forEach(function(r){
        var wps=getWP(r.zone);
        var ll=wps.map(function(p){return [p.lat,p.lng];});
        var color=STATUS_COLOR[r.status]||'#388e3c';
        layers[r.id]=[];
        var poly=L.polyline(ll,{color:color,weight:r.status==='in_progress'?5:3,opacity:r.status==='completed'?0.4:0.85,dashArray:r.status==='scheduled'?'8,6':null}).addTo(map);
        poly.bindTooltip(r.name+' ('+r.waste_type+')',{sticky:true});
        layers[r.id].push(poly);
        var sm=L.marker(ll[0],{icon:startIcon}).addTo(map);
        sm.bindPopup('<b>'+r.name+'</b><br>Inicio &bull; '+r.zone);
        layers[r.id].push(sm);
        var em=L.marker(ll[ll.length-1],{icon:endIcon}).addTo(map);
        em.bindPopup('<b>'+r.name+'</b><br>Final');
        layers[r.id].push(em);
        if(r.status==='in_progress'){
            var tLat=r.current_lat||wps[0].lat, tLng=r.current_lng||wps[0].lng;
            var truck=L.marker([tLat,tLng],{icon:truckIcon}).addTo(map);
            truck.bindPopup('<b>En ruta: '+r.name+'</b><br>'+r.waste_type);
            layers[r.id].push(truck);
            bounds.push([tLat,tLng]);
        }
        ll.forEach(function(p){bounds.push(p);});
    });
    if(bounds.length) try{map.fitBounds(bounds,{padding:[30,30],maxZoom:14});}catch(e){}
}

// Escuchar rutas enviadas desde la página padre via postMessage
window.addEventListener('message',function(e){
    if(e.data && e.data.type==='ECOLINK_ROUTES') drawRoutes(e.data.routes);
});

// Preview inicial: todas las zonas en azul punteado
var preview=[];
var i=0;
for(var z in ZONE_WP) preview.push({id:i++,name:z,zone:z,status:'scheduled',waste_type:'general',current_lat:null,current_lng:null});
drawRoutes(preview);
</script>
</body>
</html>"""

# Codificar como base64 para usarlo como src del iframe (sin problemas de CORS)
_MAP_SRC = "data:text/html;base64," + base64.b64encode(_MAP_HTML.encode()).decode()


def map_component() -> rx.Component:
    """
    Iframe autónomo con Leaflet. Al estar en su propio documento el mapa
    tiene dimensiones reales desde el primer render — no hay conflicto con React/Next.js.
    La comunicación con el estado de Reflex se hace via postMessage.
    """
    return rx.html(
        f'<iframe id="ecolink-map-frame" src="{_MAP_SRC}" '
        'style="width:100%;height:480px;border:none;border-radius:14px;'
        'box-shadow:0 4px 20px rgba(0,0,0,0.10);" allowfullscreen></iframe>'
        """
        <script>
        (function(){
            var ZONE_WP = {
                'Centro Norte': [{lat:20.9674,lng:-89.5926},{lat:20.9695,lng:-89.5940},{lat:20.9712,lng:-89.5955},{lat:20.9730,lng:-89.5965}],
                'Col. Sur':     [{lat:20.9520,lng:-89.5890},{lat:20.9505,lng:-89.5910},{lat:20.9488,lng:-89.5930},{lat:20.9470,lng:-89.5945}],
                'Zona Industrial':[{lat:20.9800,lng:-89.5600},{lat:20.9820,lng:-89.5580},{lat:20.9840,lng:-89.5560}],
                'Frac. Bello':  [{lat:20.9900,lng:-89.6100},{lat:20.9920,lng:-89.6120},{lat:20.9940,lng:-89.6140}],
                'Altabrisa':    [{lat:21.0010,lng:-89.6140},{lat:21.0030,lng:-89.6155},{lat:21.0050,lng:-89.6170}],
                'Garcia Gineres':[{lat:20.9760,lng:-89.6100},{lat:20.9775,lng:-89.6115},{lat:20.9790,lng:-89.6130}],
                'Itzimna':      [{lat:20.9850,lng:-89.6200},{lat:20.9865,lng:-89.6215},{lat:20.9880,lng:-89.6230}],
                'Uman':         [{lat:20.8900,lng:-89.7520},{lat:20.8920,lng:-89.7540},{lat:20.8940,lng:-89.7555}]
            };

            function sendRoutes(routes){
                var frame = document.getElementById('ecolink-map-frame');
                if(!frame || !frame.contentWindow) return;
                frame.contentWindow.postMessage({type:'ECOLINK_ROUTES', routes:routes}, '*');
            }

            function syncRoutes(){
                var routes = [];
                try {
                    for(var key in window){
                        try {
                            var obj = window[key];
                            if(obj && typeof obj==='object' && !Array.isArray(obj)
                               && obj.state && Array.isArray(obj.state.routes)
                               && obj.state.routes.length > 0){
                                routes = obj.state.routes;
                                break;
                            }
                        } catch(e2){}
                    }
                } catch(e){}

                if(routes.length > 0){
                    sendRoutes(routes.map(function(r){
                        return {id:r.id, name:r.name, zone:r.zone,
                                status:r.status, waste_type:r.waste_type,
                                current_lat:r.current_lat||null, current_lng:r.current_lng||null};
                    }));
                }
            }

            var frame = document.getElementById('ecolink-map-frame');
            if(frame){
                frame.addEventListener('load', function(){ setTimeout(syncRoutes, 600); });
            }
            setInterval(syncRoutes, 5000);
        })();
        </script>
        """
    )


def route_card_map(r) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.text(r.name, font_weight="700", color=C_TEXT, font_size="0.88rem"),
                    rx.match(
                        r.status,
                        ("in_progress", rx.badge("🚛 En curso",   color_scheme="orange", variant="solid", font_size="0.7rem")),
                        ("scheduled",   rx.badge("🕐 Programada", color_scheme="blue",   variant="soft",  font_size="0.7rem")),
                        ("completed",   rx.badge("✅ Lista",       color_scheme="green",  variant="soft",  font_size="0.7rem")),
                        rx.badge(r.status, color_scheme="gray", variant="soft", font_size="0.7rem"),
                    ),
                    flex_wrap="wrap", gap="0.35rem", align="center",
                ),
                rx.text("📍 " + r.zone + " · " + r.waste_type, font_size="0.75rem", color=C_MUTED),
                gap="0.2rem", align_items="flex-start", flex="1",
            ),
            rx.cond(
                r.status == "in_progress",
                rx.spinner(size="1", color="#ff6d00"),
                rx.box(),
            ),
            align="center", width="100%", gap="0.5rem",
        ),
        padding="0.75rem 1rem",
        background=rx.cond(r.status == "in_progress", "#fff3e0", C_WHITE),
        border_radius="10px",
        border=rx.cond(r.status == "in_progress", "1px solid #ffcc80", f"1px solid {C_GREEN_PALE}"),
        margin_bottom="0.4rem",
        cursor="pointer",
        _hover={"border_color": C_ACCENT},
        transition="all 0.15s",
    )


@rx.page(
    route="/map",
    title="EcoLink · Mapa en tiempo real",
    on_load=[State.on_load, State.load_dashboard_data],
)
def map_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            notification_bar(),
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("map", size=22, color=C_GREEN_MID),
                            rx.text("Mapa de Recolección",
                                    font_size="1.4rem", font_weight="800", color=C_TEXT),
                            align="center", gap="0.5rem",
                        ),
                        rx.text("Sigue los camiones en tiempo real · Mérida, Yucatán",
                                font_size="0.82rem", color=C_MUTED),
                        gap="0.15rem", align_items="flex-start",
                    ),
                    rx.spacer(),
                    rx.link(
                        rx.button(
                            rx.icon("layout-dashboard", size=14), "Dashboard",
                            variant="outline", size="2", cursor="pointer",
                            color=C_GREEN_MID, border_color=C_GREEN_MID,
                        ),
                        href="/dashboard",
                    ),
                    align="center", width="100%",
                ),
                rx.flex(
                    rx.box(map_component(), flex="1", min_width="0"),
                    rx.box(
                        rx.vstack(
                            rx.text("Rutas activas", font_weight="800", color=C_TEXT, font_size="0.95rem"),
                            rx.text(
                                State.routes.length().to_string() + " rutas registradas",
                                font_size="0.75rem", color=C_MUTED,
                            ),
                            rx.divider(border_color=C_GREEN_PALE),
                            rx.cond(
                                State.routes.length() == 0,
                                rx.center(rx.text("Sin rutas aún", color=C_MUTED, font_size="0.85rem"), padding="1rem"),
                                rx.vstack(
                                    rx.foreach(State.routes, route_card_map),
                                    width="100%", gap="0",
                                ),
                            ),
                            gap="0.5rem", width="100%",
                        ),
                        background=C_WHITE,
                        border_radius="14px",
                        padding="1rem",
                        border=f"1px solid {C_GREEN_PALE}",
                        box_shadow="0 2px 10px rgba(0,0,0,0.06)",
                        width=["100%", "100%", "280px"],
                        flex_shrink="0",
                        max_height="500px",
                        overflow_y="auto",
                    ),
                    gap="1rem",
                    wrap="wrap",
                    align="start",
                    width="100%",
                ),
                rx.box(
                    rx.hstack(
                        rx.icon("info", size=16, color=C_GREEN_MID),
                        rx.text(
                            "El mapa se actualiza automáticamente cada 5 segundos.",
                            font_size="0.8rem", color=C_MUTED,
                        ),
                        align="center", gap="0.4rem",
                    ),
                    background=C_GREEN_PALE,
                    border_radius="8px",
                    padding="0.6rem 1rem",
                    width="100%",
                ),
                gap="1rem", width="100%",
            ),
            max_width="1200px",
            margin="0 auto",
            padding="0.75rem 1.1rem 2.5rem",
            width="100%",
        ),
        background=C_BG,
        min_height="100vh",
    )