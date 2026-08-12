Kinmel — Modern Django eCommerce Marketplace



Kinmel is a full-featured eCommerce marketplace built with Django, offering a responsive shopping experience, a seller dashboard, product reviews, wishlist, order tracking, and a clean, scalable frontend architecture.



The project emphasizes production-quality UI/UX, reusable frontend components, and a well-structured Django backend — built as a software engineering internship project.



 Features



 Customer Experience

- User authentication (sign up, log in, profile management)
- Product browsing by category and brand
- Product search
- Wishlist
- Shopping cart with quantity management
- Checkout flow
- Order tracking
- Product reviews and ratings
- Fully responsive design


 Seller Dashboard
- Dashboard overview
- Add and manage products
- Product validation
- Order management
- Sales reports

 Product Experience
- Dynamic product ratings
- Customer review system
- Dedicated product detail pages
- Brand-based product organization
- Category navigation
- Horizontal product carousels

 UI / UX
- Modern, consistent design system
- Clean typography (Inter + Fraunces)
- Interactive animations and smooth transitions
- Mobile-first responsive layout
- Refined navigation and information hierarchy

 Tech Stack
| Layer | Technology |

 Backend - Python, Django 

 Frontend - HTML5, CSS3, Bootstrap 5, JavaScript, jQuery 

 Database - SQLite 

 Icons & Fonts - Font Awesome, Google Fonts (Inter & Fraunces)


 Project Structure

accounts/            authentication & user profiles

blog/                blog app

ecommercewebsite/     Django project settings

store/                core marketplace app

useradmin/            seller/admin functionality

templates/            shared templates

media/                uploaded media

manage.py

requirements.txt



\ Installation



\*1. Clone the repository\*

bash

git clone https://github.com/Dipprajwalpandey/kinmel.git

cd Kinmel

2. Create and activate a virtual environment

bash

python -m venv .venv



\# Windows

.venv\\Scripts\\activate



\# Linux / macOS

source .venv/bin/activate

```



\*\*3. Install dependencies\*\*

```bash

pip install -r requirements.txt

```



\*\*4. Apply migrations\*\*

```bash

python manage.py migrate

```



\*\*5. Run the development server\*\*

```bash

python manage.py runserver

```



Then open \*\*http://127.0.0.1:8000/\*\* in your browser.



\Roadmap

\- PostgreSQL support

\- Payment gateway integration

\- Product recommendations

\- Advanced product filtering

\- Email notifications

\- Admin analytics

\- Performance optimization

\- Docker support

\- CI/CD pipeline







\ License

This project is intended for learning, portfolio, and demonstration purposes.




\## Author

\*\*Dipprajwal Pandey\*\*

GitHub: \[github.com/Dipprajwal Pandey]https://github.com/Dipprajwalpandey

