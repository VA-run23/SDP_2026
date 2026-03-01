#import required tools
import ollama
#define your system prompt
SYSTEM_PROMPT="""
Tell me a Story
Instructions:
1.Keep Story funny
2.Keep the story not more than 2 paragraphs
"""
#converstaion list
chat_convo= {}
#conversation loop
def chat_with_ollama():
    print("welcome to story line")

    while True:
        try:
            user_input=input("User: ").strip()
        except (KeyboardInterrupt,e):
            print('User Quit')

            chat_convo.append({
                'role':'user',
                "content":user_input
            })
            
            try:
                print('chatbot  prompt Started')
                response= ollama.chat(model="phi3:mini",
                                     messages=chat_convo,
                                     options={"systems":SYSTEM_PROMPT})
                chat_convo.append({
                'role':'bot',
                "content":response
                })

                print(response)
            except:
                print('Error')

chat_with_ollama()