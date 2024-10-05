from fastapi import FastAPI, HTTPException, Depends
from schemas import OrderCreate, ProductCreate


app = FastAPI()

# эндпоинты для products
@app.post('/products/')
async def create_product(product:ProductCreate, db: Session = Depe):
    


# Endpoints for products
@app.post("/products/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/")
def read_products(db: Session = Depends(get_db)):
    return db.query(Product).all()