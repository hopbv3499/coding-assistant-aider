from utils import parse_diff

# Example usage
diff_text = """
To create the CRUD endpoints for the Partner database, we need to:

1. **Add the Partner model** in `entities.py`.
2. **Update** `database.py` to include the Partner model.
3. **Add the CRUD endpoints** in `main.py`.

Could you please add the following files to the chat so I can propose the necessary changes?

- `entities.py`
- `database.py`
Tokens: 3.3k sent, 83 received. Cost: $0.05 message, $0.05 session.



To create the CRUD endpoints for the Partner database, we need to:

1. **Add** the `Partner` model to `entities.py`.
2. **Update** `main.py` to include the CRUD endpoints for `Partner`.

Here are the *SEARCH/REPLACE* blocks:

**entities.py**
```python
<<<<<<< SEARCH
    class Config:
        orm_mode = True
=======
    class Config:
        orm_mode = True

class Partner(Base):
    __tablename__ = "partners"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    address = Column(String)

class PartnerCreate(BaseModel):
    name: str
    address: str

class PartnerRead(BaseModel):
    id: int
    name: str
    address: str

    class Config:
        orm_mode = True
>>>>>>> REPLACE
```

main.py
```python
<<<<<<< SEARCH
from entities import LoginRequest, CubeResponse, HelloResponse, LoginResponse, RenderRequest, User, UserCreate, UserRead, Page, PageCreate, PageRead
=======
from entities import LoginRequest, CubeResponse, HelloResponse, LoginResponse, RenderRequest, User, UserCreate, UserRead, Page, PageCreate, PageRead, Partner, PartnerCreate, PartnerRead
>>>>>>> REPLACE
```

main.py
```python
<<<<<<< SEARCH
    return {"detail": "Page deleted"}
=======
    return {"detail": "Page deleted"}

@app.post("/partners", response_model=PartnerRead)
def create_partner(partner: PartnerCreate, db: Session = Depends(get_db)):
    db_partner = Partner(name=partner.name, address=partner.address)
    db.add(db_partner)
    db.commit()
    db.refresh(db_partner)
    return db_partner

@app.get("/partners", response_model=List[PartnerRead])
def get_partners(db: Session = Depends(get_db)):
    partners = db.query(Partner).all()
    return partners

@app.get("/partners/{partner_id}", response_model=PartnerRead)
def get_partner(partner_id: int, db: Session = Depends(get_db)):
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if partner is None:
        raise HTTPException(status_code=404, detail="Partner not found")
    return partner

@app.put("/partners/{partner_id}", response_model=PartnerRead)
def update_partner(partner_id: int, updated_partner: PartnerCreate, db: Session = Depends(get_db)):
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if partner is None:
        raise HTTPException(status_code=404, detail="Partner not found")
    partner.name = updated_partner.name
    partner.address = updated_partner.address
    db.commit()
    db.refresh(partner)
    return partner

@app.delete("/partners/{partner_id}")
def delete_partner(partner_id: int, db: Session = Depends(get_db)):
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if partner is None:
        raise HTTPException(status_code=404, detail="Partner not found")
    db.delete(partner)
    db.commit()
    return {"detail": "Partner deleted"}
>>>>>>> REPLACE
```
Tokens: 3.9k sent, 672 received. Cost: $0.10 message, $0.15 session.
Applied edit to entities.py
Applied edit to main.py
"""

result = parse_diff(diff_text)
print(result)