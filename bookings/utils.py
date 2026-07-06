import io
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

# def generate_ticket_pdf(booking):
 
    # context = {
    #     'name': booking.user.username if booking.user else "Guest Passenger",
    #     'seat_no': booking.seat_number,
    #     'source': booking.trip.source,       
    #     'destination': booking.trip.destination, 
    #     'travel_date': booking.trip.travel_date,
    #     'price': booking.trip.price,
    # }
#     context = {
#     'name': booking.user.username if booking.user else "Guest Passenger",
#     'seat_no': booking.seat_number,
    
#     # Trip model ko current fields anusar mapping:
#     'source': booking.trip.from_location.name,       # .name ko thau ma timro Location model ko field name lekha (e.g. .title)
#     'destination': booking.trip.to_location.name,   # yaha pani exact Location model ko name field
#     'travel_date': booking.trip.date,               # Timro model ma 'date' chha
#     'price': booking.trip.price,                    # Timro model ma 'price' chha
# }
#     html_string = render_to_string('ticket_pdf.html', context)
#     result = io.BytesIO()
#     pdf = pisa.pisaDocument(io.BytesIO(html_string.encode("UTF-8")), result)
    
#     if not pdf.err:
#         response = HttpResponse(result.getvalue(), content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="ticket_{booking.id}.pdf"'
#         return response
#     return None
from weasyprint import HTML

# def generate_ticket_pdf(booking):
#     context = {
#     'name': booking.user.username if booking.user else "Guest Passenger",
#     'seat_no': booking.seat_number,
    
#     # Trip model ko current fields anusar mapping:
#     'source': booking.trip.from_location.name,       # .name ko thau ma timro Location model ko field name lekha (e.g. .title)
#     'destination': booking.trip.to_location.name,   # yaha pani exact Location model ko name field
#     'travel_date': booking.trip.date,               # Timro model ma 'date' chha
#     'price': booking.trip.price,                    # Timro model ma 'price' chha
# }
#     html_string = render_to_string('ticket_pdf.html', context)
    
#     # Simple line logic - direct response ma bytes generate garchha
#     pdf_bytes = HTML(string=html_string).write_pdf()
    
#     response = HttpResponse(pdf_bytes, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="ticket_{booking.id}.pdf"'
#     return response

def generate_ticket_pdf(booking):
    context = {
        'name': booking.user.username if booking.user else "Guest Passenger",
        'seat_no': booking.seat_number,
        'source': booking.trip.from_location.name,       
        'destination': booking.trip.to_location.name,   
        'travel_date': booking.trip.date,               
        'price': booking.trip.price,                    
    }
    
    # 1. HTML file string parsing
    html_string = render_to_string('ticket_pdf.html', context)
    
    # 2. Weasyprint single-line pdf binary converter
    pdf_bytes = HTML(string=html_string).write_pdf()
    
    # 3. Response build logic
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{booking.id}.pdf"'
    return response