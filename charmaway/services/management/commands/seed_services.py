from django.core.management.base import BaseCommand
from services.models import Service
from catalog.models import Category, Department


class Command(BaseCommand):
    help = 'Seed the database with beauty services data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting services seeding...')

        # Clear existing services
        Service.objects.all().delete()

        # Get Services department and its categories
        self.stdout.write('Getting Services department and categories...')
        try:
            services_dept = Department.objects.get(name='Servicios')
            categories_queryset = Category.objects.filter(department=services_dept)

            categories = {}
            for category in categories_queryset:
                categories[category.name] = category
                self.stdout.write(f'Found category: {category.name}')

            if not categories:
                self.stdout.write(self.style.ERROR('No categories found for Services department!'))
                self.stdout.write(self.style.WARNING('Please run seed_catalog_simple first to create the Services department and categories.'))
                return

        except Department.DoesNotExist:
            self.stdout.write(self.style.ERROR('Services department not found!'))
            self.stdout.write(self.style.WARNING('Please run seed_catalog_simple first to create the Services department.'))
            return

        # Create Services
        self.stdout.write('Creating services...')
        services_data = [
            # Asesoramiento y Consultoría
            {
                'name': 'Consultoría de Maquillaje Online - 30 min',
                'description': 'Sesión personalizada de asesoramiento de maquillaje con un experto. Descubre qué productos y técnicas son mejores para ti.',
                'category': categories['Asesoramiento y Consultoría'],
                'price': 25.00,
                'duration': '30 minutos',
                'image': 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=800',
                'is_available': True,
                'is_featured': True
            },
            {
                'name': 'Consultoría de Maquillaje Online - 60 min',
                'description': 'Sesión extendida de asesoramiento de maquillaje con análisis profundo y recomendaciones personalizadas.',
                'category': categories['Asesoramiento y Consultoría'],
                'price': 45.00,
                'offer_price': 39.99,
                'duration': '60 minutos',
                'image': 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=800',
                'is_available': True,
                'is_featured': True
            },
            {
                'name': 'Análisis de Tipo de Piel y Rutina Personalizada',
                'description': 'Análisis completo de tu tipo de piel y creación de una rutina de cuidado facial personalizada.',
                'category': categories['Asesoramiento y Consultoría'],
                'price': 35.00,
                'duration': '45 minutos',
                'image': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=800',
                'is_available': True,
                'is_featured': False
            },
            {
                'name': 'Asesoría de Color Personal',
                'description': 'Descubre qué tonos y colores te favorecen según tu tipo de piel y características personales.',
                'category': categories['Asesoramiento y Consultoría'],
                'price': 40.00,
                'duration': '50 minutos',
                'image': 'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=800',
                'is_available': True,
                'is_featured': False
            },
            {
                'name': 'Consulta Capilar Personalizada',
                'description': 'Asesoramiento experto sobre cuidado capilar, productos recomendados y rutinas para tu tipo de cabello.',
                'category': categories['Asesoramiento y Consultoría'],
                'price': 30.00,
                'duration': '40 minutos',
                'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800',
                'is_available': True,
                'is_featured': False
            },

            # Tutoriales y Masterclass
            {
                'name': 'Tutorial de Maquillaje en Vivo 1-a-1',
                'description': 'Clase personalizada donde aprenderás técnicas de maquillaje adaptadas a tu estilo y necesidades.',
                'category': categories['Tutoriales y Masterclass'],
                'price': 50.00,
                'duration': '60 minutos',
                'image': 'https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?w=800',
                'is_available': True,
                'is_featured': True
            },
            {
                'name': 'Masterclass: Smokey Eyes Perfecto',
                'description': 'Aprende a crear el smokey eyes perfecto con técnicas profesionales paso a paso.',
                'category': categories['Tutoriales y Masterclass'],
                'price': 35.00,
                'duration': '45 minutos',
                'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800',
                'is_available': True,
                'is_featured': False
            },
            {
                'name': 'Masterclass: Técnicas de Contouring',
                'description': 'Domina las técnicas de contouring y aprende a resaltar tus mejores rasgos.',
                'category': categories['Tutoriales y Masterclass'],
                'price': 35.00,
                'duration': '45 minutos',
                'image': 'https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?w=800',
                'is_available': True,
                'is_featured': False
            },
            {
                'name': 'Clase: Cuidado de la Piel - Rutina Coreana',
                'description': 'Aprende la famosa rutina coreana de cuidado de la piel en 10 pasos.',
                'category': categories['Tutoriales y Masterclass'],
                'price': 30.00,
                'duration': '40 minutos',
                'image': 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=800',
                'is_available': True,
                'is_featured': False
            },
            {
                'name': 'Masterclass: Maquillaje de Novia',
                'description': 'Técnicas especializadas para lograr un maquillaje de novia perfecto que dure todo el día.',
                'category': categories['Tutoriales y Masterclass'],
                'price': 55.00,
                'duration': '90 minutos',
                'image': 'https://images.unsplash.com/photo-1515688594390-b649af70d282?w=800',
                'is_available': True,
                'is_featured': True
            },

            # Servicios de Entrega
            {
                'name': 'Gift Wrapping Premium',
                'description': 'Envoltorio de regalo premium con papel de alta calidad, lazo elegante y tarjeta personalizada.',
                'category': categories['Servicios de Entrega'],
                'price': 5.99,
                'duration': '',
                'image': 'https://images.unsplash.com/photo-1513885535751-8b9238bd345a?w=800',
                'is_available': True,
                'is_featured': False
            },
            {
                'name': 'Tarjeta de Felicitación Personalizada',
                'description': 'Añade una tarjeta de felicitación con tu mensaje personalizado al pedido.',
                'category': categories['Servicios de Entrega'],
                'price': 2.99,
                'duration': '',
                'image': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800',
                'is_available': True,
                'is_featured': False
            },
            {
                'name': 'Caja de Regalo Premium',
                'description': 'Caja de regalo de lujo perfecta para ocasiones especiales, incluye papel de seda y detalles elegantes.',
                'category': categories['Servicios de Entrega'],
                'price': 8.99,
                'duration': '',
                'image': 'https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=800',
                'is_available': True,
                'is_featured': False
            },
            {
                'name': 'Entrega Express 24h',
                'description': 'Recibe tu pedido en 24 horas (solo disponible para determinadas zonas).',
                'category': categories['Servicios de Entrega'],
                'price': 12.99,
                'duration': '',
                'image': 'https://images.unsplash.com/photo-1566576721346-d4a3b4eaeb55?w=800',
                'is_available': True,
                'is_featured': True
            },
            {
                'name': 'Entrega en Fecha Específica',
                'description': 'Elige el día exacto en que quieres recibir tu pedido (hasta 30 días de antelación).',
                'category': categories['Servicios de Entrega'],
                'price': 6.99,
                'duration': '',
                'image': 'https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=800',
                'is_available': True,
                'is_featured': False
            },

            # Personalización
            {
                'name': 'Personalización de Neceser con Iniciales',
                'description': 'Bordado de iniciales en neceser o estuche de maquillaje (hasta 3 letras).',
                'category': categories['Personalización'],
                'price': 9.99,
                'duration': '3-5 días',
                'image': 'https://images.unsplash.com/photo-1522673607200-164d1b6ce486?w=800',
                'is_available': True,
                'is_featured': False
            },
            {
                'name': 'Kit de Muestras Premium (3 fragancias)',
                'description': 'Recibe 3 muestras de fragancias de tu elección para probar antes de comprar.',
                'category': categories['Personalización'],
                'price': 7.99,
                'duration': '',
                'image': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=800',
                'is_available': True,
                'is_featured': False
            },
            {
                'name': 'Kit de Muestras Premium (5 productos)',
                'description': 'Selección de 5 muestras de productos de cuidado o maquillaje para descubrir nuevas opciones.',
                'category': categories['Personalización'],
                'price': 12.99,
                'duration': '',
                'image': 'https://images.unsplash.com/photo-1596704017254-9b121068fb31?w=800',
                'is_available': True,
                'is_featured': True
            },

            # Suscripciones
            {
                'name': 'Beauty Box Mensual Personalizada',
                'description': 'Caja mensual con productos sorpresa adaptados a tus preferencias y tipo de piel.',
                'category': categories['Suscripciones'],
                'price': 29.99,
                'duration': 'Mensual',
                'image': 'https://images.unsplash.com/photo-1522338242992-e1a54906a8da?w=800',
                'is_available': True,
                'is_featured': True
            },
            {
                'name': 'Club VIP - Membresía Trimestral',
                'description': 'Acceso a descuentos exclusivos, envío gratuito y productos en preventa por 3 meses.',
                'category': categories['Suscripciones'],
                'price': 49.99,
                'duration': '3 meses',
                'image': 'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=800',
                'is_available': True,
                'is_featured': True
            },
            {
                'name': 'Club VIP - Membresía Anual',
                'description': 'Acceso a descuentos exclusivos, envío gratuito, productos en preventa y regalos por 12 meses.',
                'category': categories['Suscripciones'],
                'price': 159.99,
                'offer_price': 139.99,
                'duration': '12 meses',
                'image': 'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=800',
                'is_available': True,
                'is_featured': True
            },
            {
                'name': 'Skincare Box Mensual',
                'description': 'Caja mensual especializada en productos de cuidado facial seleccionados por expertos.',
                'category': categories['Suscripciones'],
                'price': 35.99,
                'duration': 'Mensual',
                'image': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=800',
                'is_available': True,
                'is_featured': False
            },

            # OUT OF STOCK SERVICES
            # Asesoramiento y Consultoría - Agotado
            {
                'name': 'Análisis de Colorimetría Presencial',
                'description': 'Sesión presencial de análisis completo de colorimetría para determinar tu paleta de colores ideal. Incluye guía digital.',
                'category': categories['Asesoramiento y Consultoría'],
                'price': 85.00,
                'duration': '90 minutos',
                'image': 'https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?w=800',
                'is_available': False,
                'is_featured': False
            },
            {
                'name': 'Consultoría de Imagen Completa',
                'description': 'Servicio integral de consultoría de imagen incluyendo análisis facial, colorimetría y recomendaciones de maquillaje.',
                'category': categories['Asesoramiento y Consultoría'],
                'price': 120.00,
                'offer_price': 99.99,
                'duration': '2 horas',
                'image': 'https://images.unsplash.com/photo-1487412947147-5cebf100ffc2?w=800',
                'is_available': False,
                'is_featured': False
            },
            {
                'name': 'Asesoría de Cuidado Anti-Edad',
                'description': 'Consultoría especializada en rutinas y productos anti-edad personalizados según tu tipo de piel.',
                'category': categories['Asesoramiento y Consultoría'],
                'price': 55.00,
                'duration': '60 minutos',
                'image': 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=800',
                'is_available': False,
                'is_featured': False
            },

            # Tutoriales y Masterclass - Agotado
            {
                'name': 'Masterclass Grupal: Maquillaje de Fiesta',
                'description': 'Clase grupal donde aprenderás a crear looks espectaculares para ocasiones especiales. Máximo 8 personas.',
                'category': categories['Tutoriales y Masterclass'],
                'price': 75.00,
                'offer_price': 65.00,
                'duration': '2 horas',
                'image': 'https://images.unsplash.com/photo-1596704017254-9b121068fb31?w=800',
                'is_available': False,
                'is_featured': True
            },
            {
                'name': 'Tutorial: Maquillaje Editorial',
                'description': 'Aprende técnicas avanzadas de maquillaje editorial y artístico con una maquilladora profesional.',
                'category': categories['Tutoriales y Masterclass'],
                'price': 65.00,
                'duration': '90 minutos',
                'image': 'https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?w=800',
                'is_available': False,
                'is_featured': False
            },
            {
                'name': 'Clase: Cuidado de Pestañas y Cejas',
                'description': 'Aprende a cuidar, peinar y maquillar tus pestañas y cejas como una profesional.',
                'category': categories['Tutoriales y Masterclass'],
                'price': 28.00,
                'duration': '35 minutos',
                'image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800',
                'is_available': False,
                'is_featured': False
            },

            # Servicios de Entrega - Agotado
            {
                'name': 'Entrega Express Same Day',
                'description': 'Recibe tu pedido el mismo día (solo disponible en zonas premium de Madrid y Barcelona). Pedido antes de las 14h.',
                'category': categories['Servicios de Entrega'],
                'price': 19.99,
                'duration': '',
                'image': 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800',
                'is_available': False,
                'is_featured': False
            },
            {
                'name': 'Caja de Regalo Edición Limitada',
                'description': 'Caja de regalo de edición limitada con diseño exclusivo y detalles premium. Solo disponible en temporada navideña.',
                'category': categories['Servicios de Entrega'],
                'price': 14.99,
                'duration': '',
                'image': 'https://images.unsplash.com/photo-1513885535751-8b9238bd345a?w=800',
                'is_available': False,
                'is_featured': False
            },

            # Personalización - Agotado
            {
                'name': 'Grabado Láser en Compacto de Maquillaje',
                'description': 'Personaliza tu compacto de maquillaje con grabado láser de texto o diseño simple.',
                'category': categories['Personalización'],
                'price': 15.99,
                'duration': '5-7 días',
                'image': 'https://images.unsplash.com/photo-1596704017254-9b121068fb31?w=800',
                'is_available': False,
                'is_featured': False
            },
            {
                'name': 'Paleta de Sombras Personalizada',
                'description': 'Crea tu propia paleta de sombras eligiendo hasta 12 tonos de nuestra colección completa.',
                'category': categories['Personalización'],
                'price': 45.00,
                'duration': '7-10 días',
                'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800',
                'is_available': False,
                'is_featured': True
            },
            {
                'name': 'Set de Brochas con Estuche Personalizado',
                'description': 'Set de brochas profesionales con estuche bordado con tu nombre o iniciales.',
                'category': categories['Personalización'],
                'price': 65.00,
                'offer_price': 55.00,
                'duration': '10-14 días',
                'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800',
                'is_available': False,
                'is_featured': False
            },

            # Suscripciones - Agotado
            {
                'name': 'Makeup Artist Box - Edición Pro',
                'description': 'Caja trimestral exclusiva con productos profesionales de alta gama para maquilladores. Edición limitada.',
                'category': categories['Suscripciones'],
                'price': 99.99,
                'duration': 'Trimestral',
                'image': 'https://images.unsplash.com/photo-1522338242992-e1a54906a8da?w=800',
                'is_available': False,
                'is_featured': True
            },
            {
                'name': 'Fragrance Club - Membresía Mensual',
                'description': 'Recibe cada mes una fragancia de diseñador de tamaño completo rotativa. Explora nuevos aromas constantemente.',
                'category': categories['Suscripciones'],
                'price': 45.00,
                'duration': 'Mensual',
                'image': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=800',
                'is_available': False,
                'is_featured': False
            },
        ]

        services_created = 0
        for service_data in services_data:
            Service.objects.create(**service_data)
            services_created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {services_created} services!'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} service categories'))
        self.stdout.write(self.style.SUCCESS('Services seeding completed successfully!'))
