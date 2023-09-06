import json
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI, Response, Request, Path, Body
from pydantic import BaseModel

cred = credentials.Certificate("training-first-app-63180-firebase-adminsdk-wqgwl-241b7b5bbc.json")
firebase_admin.initialize_app(cred)
app = FastAPI()
db = firestore.client()
collectionContacts = db.collection('contacts')

@app.get("/")
def read_root():
         return {"message": "First App - API"}

@app.get("/contatos")
def get_contacts():
       docs = collectionContacts.stream()
       contacs = []
       for doc in docs:
              contact = doc.to_dict()
              contact['db_id'] = doc.id
              contacs.append(contact)
       return contacs

class UpdateContactRequest(BaseModel):
    firstName: str = None
    lastName: str = None
    email: str = None

@app.put("/contatos/{contact_id}")
async def update_contact(contact_id: str, contact_update: UpdateContactRequest):

    # Para atualizar um contato, é necessário pegar o db_id
    # Para pegar o db_id, faça o request get acima, para assim pegar o db_id
    # Após isso aplique o db_id na região onde é contact_id na URL direta
    # Exemplo: http://127.0.0.1:8000/contatos/5DXktRAkfseL7V3HXfxn

    contact_ref = db.collection('contacts').document(contact_id)
    contact = contact_ref.get()
    
    if contact.exists:
        contact_ref.update({
            'firstName': contact_update.firstName,
            'lastName': contact_update.lastName,
            'email': contact_update.email
        })
        return {"message": "Contato atualizado com sucesso!"}
    else:
        return {"message": "Contato não encontrado"}

@app.delete("/contatos/{contact_id}")
async def delete_contact(contact_id: str):
      
    # Para deletar um contato, é necessário pegar o db_id
    # Para pegar o db_id, faça o request get acima, para assim pegar o db_id
    # Após isso aplique o db_id na região onde é contact_id na URL direta
    # Exemplo: http://127.0.0.1:8000/contatos/5DXktRAkfseL7V3HXfxn

      contact_del = db.collection('contacts').document(contact_id)

      contactEx = contact_del.get()
      if contactEx.exists:
            contact_del.delete()
            return {"message": "Contato excluído com sucesso!"}
      
      return {"message": "Contato não encontrado"}


@app.post("/contatos")
async def create_contact(request: Request, reponse: Response):
        params = await request.json()
        print('\n ---- Params ----\n', params, '\n---- fim params ----\n')
        contact = Contact(**params)

        if not contact.email:
            reponse.status_code = 403
            return {'message': 'Email is required'}

        has_contact = collectionContacts.where("email","==", contact.email).get()
        if has_contact:
               reponse.status_code = 403
               return {'message': 'Contact already exists'}
        
        is_created = collectionContacts.document().set(contact.dict())
        if is_created:
               return {'message': 'Criado com sucesso'}
        
        reponse.status_code = 403
        return{'message': 'Error'}

class Contact(BaseModel):
       contact_id: int;
       firstName: str;
       lastName: str;
       email: str;
       properties: list[str];