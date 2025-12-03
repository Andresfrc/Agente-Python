import ollama
from datetime import datetime

class Agente:
    def __init__(self, model="gemma3:1b", max_history=10):
        self.model = model
        self.conversation_history = []
        self.max_history = max_history
        self.topics_proposed = []
        self.system_prompt = """Eres un agente conversacional inteligente y amigable.
        Tu objetivo es tener una conversacion interesante y significativa con el usuario.
        Habilidades:
        -Propones temas de conversacion relevantes e interesantes
        -Mantienes conversaciones naturales y fluidas
        -Puedes profundizar en temas complejos
        -Eres curioso y haces preguntas relevantes
        -Te adaptas al estilo de la conversacion del usuario

        Cuando propongas temas, considera:
        -Intereses previos mostrados en la conversacion
        -Temas actuales y relevantes
        -Balance entre profundidad y accesibilidad
        -Diversidad de areas (ciencia, cultura, tecnologia, etc.)

        Responde siempre en español de forma natural y conversacional.
        """

    def add_to_history(self, role, content):
        self.conversation_history.append({
            "role": role,
            "content": content
        })

        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]

    def get_messages(self):
        messages = [{"role":"system", "content": self.system_prompt}]
        messages.extend(self.conversation_history)
        return messages

    def propose_topics(self):
        prompt = """Propon un tema de conversacion interesante y atractivo.
        Considera:
        -Que sea algo que genere una buena discusion
        -Que sea algo accesible y profundo
        -Que despierte curiosidad e interes

        Formato: Presenta el tema en 3-5 lineas maximo, de forma entusiasta y con una pregunta para empezar.
        """

        self.add_to_history("user", prompt)
        response = ollama.chat(
            model=self.model,
            messages=self.get_messages()
        )

        topic = response['message']['content']
        self.add_to_history("assistant", topic)
        self.topics_proposed.append({
            "topic": topic,
            "timestamp": datetime.now().isoformat()
        })
        return topic

    def chat(self, user_message):
        self.add_to_history("user", user_message)

        try:
            response = ollama.chat(
                model=self.model,
                messages=self.get_messages()
            )
            assistant_message = response['message']['content']
            self.add_to_history("assistant", assistant_message)
            return assistant_message
        except Exception as e:
            return f"Error al comunicarse con el orquestador: {str(e)}"

    def get_conversation_summary(self):
        if not self.conversation_history:
            return "No existe conversacion activa"

        total_message = len(self.conversation_history)
        user_message = len([m for m in self.conversation_history if m['role']=='user'])

        return f"""
        Resumen de la conversacion:
        - Total de mensajes: {total_message}
        - Mensajes de usuario: {user_message}
        - Temas propuestos: {len(self.topics_proposed)}
        """

    def reset_conversation(self):
        self.conversation_history = []
        self.topics_proposed = []
        print("Reiniciando la conversación...")

# ---------------- MAIN ----------------

def main():
    print("Iniciando Agente")
    agent = Agente(model="llama3.1")
    
    print("Pille el tema: \n")
    initial_topic = agent.propose_topics()
    print(f"Agente: \n{initial_topic}")

    while True:
        try:
            user_input = input("Yo: ").strip()

            if not user_input:
                continue

            if user_input.lower() == 'salir':
                print("Agente: ¡Hasta luego!")
                break

            elif user_input.lower() == 'proponer':
                print("Pille el tema: \n")
                topic = agent.propose_topics()
                print(f"Agente: \n{topic}")

            elif user_input.lower() == 'resumen':
                print(agent.get_conversation_summary())

            elif user_input.lower() == 'reiniciar':
                agent.reset_conversation()
                print("Agente: Otra vez iniciamos")

            else:
                print("Agente: ", end="", flush=True)
                response = agent.chat(user_input)
                print(response)

        except KeyboardInterrupt:
            print("\nAgente: Conversación finalizada.")
            break

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()