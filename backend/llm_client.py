class FakeLLMClient:
    """
    Cliente LLM de prueba que devuelve un JSON fijo para poder probar la pipeline
    sin conectarse a ningún modelo real.
    """
    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 4000) -> str:
        # Devuelve un JSON mínimo válido de ProjectFull (manifest + 2 scenes)
        return '''
        {
          "manifest": {
            "project_id": "auto_test",
            "titulo": "Demo Fake",
            "logline": "Una demo generada por FakeLLMClient.",
            "objetivo_contenido": "entretener",
            "audiencia_principal": "creadores de contenido",
            "plataformas_destino": ["tiktok","youtube_short"],
            "duracion_objetivo_segundos": 90,
            "ratio_aspecto": "9:16",
            "estilo_visual_base": "realista_cinematico_demo",
            "nivel_control": "simple",
            "script_original": "SCRIPT DE PRUEBA"
          },
          "scenes": [
            {
              "scene_id": "scene_01",
              "orden": 1,
              "peso_narrativo": "medio",
              "descripcion_narrativa": "El protagonista entra en la ciudad sumergida.",
              "objetivo_emocional": "anticipacion",
              "duracion_estimada_segundos": 40.0,
              "estilo_visual_objetivo": "realista_cinematico_azul",
              "tipo_plano_dominante": "plano_general",
              "quality_budget": "medio",
              "image_model_profile": "juggernaut_cinematic_v1",
              "tipo_accion": "accion_camara",
              "render_strategy": "preview_then_final",
              "video_preview_model": "ltx_standard_v1",
              "video_final_model": "mochi_cinematic_v1"
            },
            {
              "scene_id": "scene_02",
              "orden": 2,
              "peso_narrativo": "climax",
              "descripcion_narrativa": "Primer plano del protagonista mientras toma la decisión final.",
              "objetivo_emocional": "tension",
              "duracion_estimada_segundos": 50.0,
              "estilo_visual_objetivo": "realista_cinematico_azul",
              "tipo_plano_dominante": "primer_plano",
              "quality_budget": "alto",
              "image_model_profile": "juggernaut_cinematic_v1",
              "tipo_accion": "monologo",
              "render_strategy": "preview_then_final",
              "video_preview_model": "ltx_standard_v1",
              "video_final_model": "hunyuan_hero_v1"
            }
          ]
        }
        '''
