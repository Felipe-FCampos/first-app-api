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

"""@app.put("/contatos/{contact_id}/{new_first_name}")
async def update_contact(contact_id: str, new_first_name: str):

    contact_id_str = str(contact_id)
    contact_ref = db.collection('contacts').document(contact_id_str)
    contact = contact_ref.get()
    
    if contact.exists:
        contact_ref.update({'firstName': new_first_name})
        return {"message": "Nome atualizado com sucesso!"}
    else:
        return {"message": "Contato não encontrado"}
    
@app.put("/contatos/{contact_id}/{new_last_name}")
async def update_contact_lastname(contact_id: str, new_last_name: str):

    contact_id_str = str(contact_id)
    contact_ref = db.collection('contacts').document(contact_id_str)
    contact = contact_ref.get()
    
    if contact.exists:
        contact_ref.update({'lastName': new_last_name})
        return {"message": "Ultimo nome atualizado com sucesso!"}
    else:
        return {"message": "Contato não encontrado"}
    
@app.put("/contatos/{contact_id}/{new_email}")
async def update_contact_email(contact_id: str, new_email: str):

    contact_id_str = str(contact_id)
    contact_ref = db.collection('contacts').document(contact_id_str)
    contact = contact_ref.get()
    
    if contact.exists:
        contact_ref.update({'email': new_email})
        return {"message": "Email atualizado com sucesso!"}
    else:
        return {"message": "Contato não encontrado"}"""

class ContactUpdateModel:
    def __init__(self, first_name: str = None, last_name: str = None, email: str = None):
        self.firsNname = first_name
        self.lastName = last_name
        self.email = email

@app.put("/contatos/{contact_id}")
async def update_contact(
    contact_id: str = Path(..., title="ID do Contato"),
    contact_update: ContactUpdateModel = Body(..., title="Dados do Contato a serem Atualizados"),
):
    if contact_id not in db:
        return {"message": "Contato não encontrado"}

    contact = db[contact_id]

    if contact_update.firstName is not None:
        contact.firstName = contact_update.firstName

    if contact_update.lastName is not None:
        contact.lastName = contact_update.lastName

    if contact_update.email is not None:
        contact.email = contact_update.email

    return {"message": "Contato atualizado com sucesso!"}


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
       