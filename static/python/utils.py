from email.message import EmailMessage
import ssl
import smtplib
from decouple import config

BUSSINESS_EMAIL = config('EMAIL_HOST_USER')
BUSSINESS_PASSWORD = config('EMAIL_HOST_PASSWORD')

def send_email(order, product_orders):

    to = order.shipping_address.email
    subject = "[noreply] Pedido de DTechnology confirmado"

    separator = "----------------------------------------\n"
    ref = "Referencia del pedido: " + str(order.ref_code) + "\n" 
    date = "Fecha del pedido: " + parse_date(str(order.ordered_date)) + "\n"
    address = "Dirección de envío: " + order.shipping_address.get_address() + "\n"
    type_payment = "Tipo de pago: " + str(order.shipping_address.payment) + "\n"

    products = "\nProductos comprados: \n"
    for product_order in product_orders:
        product = product_order.product.title
        quantity = product_order.quantity
        unit_price = product_order.product.get_actual_price()
        total_price = unit_price * quantity
        products += "   · " + product + " | Precio unitario: " + str(unit_price) + "€ | Cantidad: " + str(quantity) + " | Precio total: " + str(total_price) + "€\n"
      

    total = "\nTotal de la compra: " + str(order.get_total()) + "€" + "\n"    


    body = separator + ref + address + date + type_payment + products + total + separator 

    msg = EmailMessage()
    msg['From'] = BUSSINESS_EMAIL
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(BUSSINESS_EMAIL, BUSSINESS_PASSWORD)
        smtp.sendmail(BUSSINESS_EMAIL, to, msg.as_string())

def parse_date(datetime):
    date = datetime.split(" ")[0]
    time = datetime.split(" ")[1].split(".")[0]

    day = date.split("-")[2]
    month = date.split("-")[1]
    year = date.split("-")[0]

    return day + "/" + month + "/" + year + " " + time