from django.core.management.base import BaseCommand
from catalog.models import Brand, Category, Product, ProductImage, ProductSize


class Command(BaseCommand):
    help = 'Seed the database with cosmetic products data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting catalog seeding...')

        # Clear existing data
        ProductImage.objects.all().delete()
        ProductSize.objects.all().delete()
        Product.objects.all().delete()
        Brand.objects.all().delete()
        Category.objects.all().delete()

        # Create Brands (Extended to 25 brands)
        brands_data = [
            {'name': 'L\'Oréal Paris', 'description': 'Líder mundial en productos de belleza con fórmulas innovadoras para todas las necesidades de belleza', 'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400'},
            {'name': 'Maybelline', 'description': 'Marca de cosméticos neoyorquina que ofrece productos de maquillaje asequibles y de moda', 'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400'},
            {'name': 'Garnier', 'description': 'Productos naturales de cuidado de belleza para piel y cabello con ingredientes botánicos', 'image': 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=400'},
            {'name': 'Nivea', 'description': 'Marca de cuidado de la piel de confianza con más de 100 años de experiencia en protección cutánea', 'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400'},
            {'name': 'The Ordinary', 'description': 'Formulaciones clínicas para el cuidado de la piel con integridad y transparencia', 'image': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400'},
            {'name': 'CeraVe', 'description': 'Cuidado de la piel desarrollado por dermatólogos con ceramidas esenciales', 'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400'},
            {'name': 'NYX Professional Makeup', 'description': 'Maquillaje de calidad profesional a precios asequibles con colores atrevidos', 'image': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400'},
            {'name': 'Neutrogena', 'description': 'Cuidado de la piel recomendado por dermatólogos para una piel sana y hermosa', 'image': 'https://images.unsplash.com/photo-1570554886111-e80fcca6a029?w=400'},
            {'name': 'Revlon', 'description': 'Marca icónica de belleza que ofrece cosméticos de color y cuidado capilar', 'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400'},
            {'name': 'La Roche-Posay', 'description': 'Cuidado de la piel farmacéutico francés recomendado por dermatólogos en todo el mundo', 'image': 'https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=400'},
            {'name': 'Vichy', 'description': 'Cuidado de la piel francés enriquecido con agua mineralizante volcánica', 'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400'},
            {'name': 'Clinique', 'description': 'Cuidado de la piel y maquillaje sin fragancia, probado contra alergias y desarrollado por dermatólogos', 'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400'},
            {'name': 'MAC Cosmetics', 'description': 'Marca de maquillaje artístico profesional con productos audaces y altamente pigmentados', 'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400'},
            {'name': 'Estée Lauder', 'description': 'Cuidado de la piel y maquillaje de lujo con tecnología avanzada antienvejecimiento', 'image': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400'},
            {'name': 'Lancôme', 'description': 'Marca de belleza de lujo francesa con cuidado de la piel innovador y fragancias', 'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400'},
            {'name': 'Benefit Cosmetics', 'description': 'Productos de belleza divertidos y femeninos con soluciones de belleza instantáneas', 'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400'},
            {'name': 'Urban Decay', 'description': 'Maquillaje audaz y moderno con fórmulas de alto rendimiento', 'image': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400'},
            {'name': 'Kiehl\'s', 'description': 'Cuidado natural de la piel con fórmulas eficaces desde 1851', 'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400'},
            {'name': 'The Body Shop', 'description': 'Productos de belleza de inspiración natural producidos éticamente', 'image': 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=400'},
            {'name': 'Bioderma', 'description': 'Experiencia dermatológica en cuidado de la piel suave y efectivo', 'image': 'https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=400'},
            {'name': 'Nuxe', 'description': 'Cosmética natural francesa que combina naturaleza e innovación', 'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400'},
            {'name': 'Rimmel London', 'description': 'Maquillaje estilo londinense con precios asequibles y colores de moda', 'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400'},
            {'name': 'Dove', 'description': 'Cuidado de belleza real con fórmulas hidratantes para todos', 'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=400'},
            {'name': 'Olay', 'description': 'Cuidado de la piel antienvejecimiento innovador respaldado por la ciencia', 'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400'},
            {'name': 'Catrice', 'description': 'Cosméticos de moda asequibles con alta calidad', 'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400'},
        ]

        brands = {}
        for brand_data in brands_data:
            brand = Brand.objects.create(**brand_data)
            brands[brand.name] = brand
            self.stdout.write(f'Created brand: {brand.name}')

        # Create Categories (Extended to 12 categories)
        categories_data = [
            {'name': 'Cuidado Facial', 'description': 'Gama completa de productos de cuidado facial para todo tipo de pieles', 'image': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400'},
            {'name': 'Maquillaje', 'description': 'Cosméticos de color para ojos, labios y rostro', 'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400'},
            {'name': 'Cuidado Capilar', 'description': 'Champús, acondicionadores y tratamientos para un cabello saludable', 'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=400'},
            {'name': 'Cuidado Corporal', 'description': 'Hidratantes, lociones y tratamientos para la piel del cuerpo', 'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=400'},
            {'name': 'Perfumes', 'description': 'Fragancias para hombres y mujeres', 'image': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400'},
            {'name': 'Protección Solar', 'description': 'Protectores solares y productos aftersun para protección de la piel', 'image': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400'},
            {'name': 'Cuidado de Uñas', 'description': 'Esmaltes de uñas, tratamientos y accesorios', 'image': 'https://images.unsplash.com/photo-1610992015732-2449b76344bc?w=400'},
            {'name': 'Cuidado Masculino', 'description': 'Productos especializados para el cuidado y aseo masculino', 'image': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400'},
            {'name': 'Cuidado de Ojos', 'description': 'Tratamientos y cremas para el delicado contorno de ojos', 'image': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400'},
            {'name': 'Cuidado de Labios', 'description': 'Bálsamos, tratamientos y cuidado para labios', 'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400'},
            {'name': 'Anti-Edad', 'description': 'Productos avanzados para combatir los signos del envejecimiento', 'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400'},
            {'name': 'Baño y Ducha', 'description': 'Geles, jabones y productos para baño y ducha', 'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=400'},
        ]

        categories = {}
        for category_data in categories_data:
            category = Category.objects.create(**category_data)
            categories[category.name] = category
            self.stdout.write(f'Created category: {category.name}')

        # Create Products (Extended to 100+ products)
        products_data = [
            # === CUIDADO FACIAL === (25 productos)
            {
                'name': 'Sérum de Ácido Hialurónico 2% + B5',
                'description': 'Fórmula de soporte de hidratación con ácido hialurónico y vitamina B5 para una piel tersa y de aspecto saludable',
                'price': 8.99, 'offer_price': 6.99, 'brand': brands['The Ordinary'], 'category': categories['Cuidado Facial'],
                'stock': 150, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 150}]
            },
            {
                'name': 'Limpiador Facial Hidratante',
                'description': 'Limpiador suave con ceramidas y ácido hialurónico para piel normal a seca',
                'price': 14.99, 'brand': brands['CeraVe'], 'category': categories['Cuidado Facial'],
                'stock': 200, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '237ml', 'stock': 100}, {'size': '473ml', 'stock': 100}]
            },
            {
                'name': 'Crema de Día Anti-Arrugas Revitalift',
                'description': 'Hidratante anti-edad con pro-retinol y elastina para reducir las arrugas',
                'price': 18.99, 'offer_price': 15.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Cuidado Facial'],
                'stock': 120, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 120}]
            },
            {
                'name': 'Agua Micelar Limpiadora',
                'description': 'Limpiador todo en uno y desmaquillante para todo tipo de pieles',
                'price': 9.99, 'brand': brands['Garnier'], 'category': categories['Cuidado Facial'],
                'stock': 250, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '400ml', 'stock': 250}]
            },
            {
                'name': 'Sérum de Niacinamida 10% + Zinc 1%',
                'description': 'Sérum equilibrante y clarificante para piel propensa a imperfecciones',
                'price': 7.99, 'brand': brands['The Ordinary'], 'category': categories['Cuidado Facial'],
                'stock': 180, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 180}]
            },
            {
                'name': 'Loción Hidratante Dramatically Different+',
                'description': 'Hidratación desarrollada por dermatólogos que fortalece la barrera cutánea',
                'price': 32.00, 'brand': brands['Clinique'], 'category': categories['Cuidado Facial'],
                'stock': 95, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '125ml', 'stock': 95}]
            },
            {
                'name': 'Crema Anti-Imperfecciones Effaclar Duo+',
                'description': 'Cuidado correctivo anti-imperfecciones para piel propensa al acné',
                'price': 19.99, 'brand': brands['La Roche-Posay'], 'category': categories['Cuidado Facial'],
                'stock': 110, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '40ml', 'stock': 110}]
            },
            {
                'name': 'Suspensión de Vitamina C 23% + Esferas de AH 2%',
                'description': 'Vitamina C directa con ácido L-ascórbico para iluminar la piel',
                'price': 10.99, 'brand': brands['The Ordinary'], 'category': categories['Cuidado Facial'],
                'stock': 140, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 140}]
            },
            {
                'name': 'Crema Hidratante',
                'description': 'Hidratante rica para rostro y cuerpo para piel seca a muy seca',
                'price': 18.99, 'brand': brands['CeraVe'], 'category': categories['Cuidado Facial'],
                'stock': 165, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '340g', 'stock': 165}]
            },
            {
                'name': 'Concentrado de Recuperación Nocturna',
                'description': 'Sérum nocturno con aceites esenciales para la recuperación y luminosidad de la piel',
                'price': 52.00, 'brand': brands['Kiehl\'s'], 'category': categories['Cuidado Facial'],
                'stock': 75, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 75}]
            },
            {
                'name': 'Crema Facial Ultra',
                'description': 'Crema hidratante de 24 horas con glicoproteína glacial',
                'price': 34.00, 'brand': brands['Kiehl\'s'], 'category': categories['Cuidado Facial'],
                'stock': 88, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 88}]
            },
            {
                'name': 'Agua Micelar Sensibio H2O',
                'description': 'Agua micelar limpiadora y desmaquillante suave para piel sensible',
                'price': 16.99, 'brand': brands['Bioderma'], 'category': categories['Cuidado Facial'],
                'stock': 200, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '500ml', 'stock': 200}]
            },
            {
                'name': 'Gel Rehidratante de Hidratación Profunda Aquasource',
                'description': 'Gel hidratante fresco con Life Plankton para 48h de hidratación',
                'price': 38.00, 'brand': brands['Vichy'], 'category': categories['Cuidado Facial'],
                'stock': 92, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 92}]
            },
            {
                'name': 'Concentrado Renovador Profundo Prodigy Cellglow',
                'description': 'Sérum lujoso con extracto de edelweiss para una piel radiante',
                'price': 49.90, 'brand': brands['Nuxe'], 'category': categories['Cuidado Facial'],
                'stock': 65, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 65}]
            },
            {
                'name': 'Crema Hidratante Nocturna Regenerist Retinol24',
                'description': 'Hidratante con retinol sin fragancia para una piel suave y luminosa',
                'price': 28.99, 'offer_price': 24.99, 'brand': brands['Olay'], 'category': categories['Cuidado Facial'],
                'stock': 105, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 105}]
            },
            {
                'name': 'Solución Exfoliante de Ácido Láctico 10% + AH',
                'description': 'Sérum exfoliante con ácido láctico para una piel más suave y luminosa',
                'price': 8.99, 'brand': brands['The Ordinary'], 'category': categories['Cuidado Facial'],
                'stock': 135, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 135}]
            },
            {
                'name': 'Limpiador Facial Espumoso',
                'description': 'Limpiador espumoso refrescante para piel normal a grasa',
                'price': 13.99, 'brand': brands['CeraVe'], 'category': categories['Cuidado Facial'],
                'stock': 190, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '236ml', 'stock': 190}]
            },
            {
                'name': 'Sérum de Vitamina C Pura SkinCeuticals',
                'description': 'Sérum de vitamina C de alta potencia para beneficios anti-edad visibles',
                'price': 45.00, 'brand': brands['Vichy'], 'category': categories['Cuidado Facial'],
                'stock': 70, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '20ml', 'stock': 70}]
            },
            {
                'name': 'Sérum de Ácido Hialurónico Mineral 89',
                'description': 'Potenciador diario fortificante y rellenador con 89% de agua volcánica de Vichy',
                'price': 29.99, 'brand': brands['Vichy'], 'category': categories['Cuidado Facial'],
                'stock': 115, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 115}]
            },
            {
                'name': 'Cuidado Diario de Doble Corrección Normaderm Phytosolution',
                'description': 'Hidratante matificante para piel grasa propensa al acné',
                'price': 17.99, 'brand': brands['Vichy'], 'category': categories['Cuidado Facial'],
                'stock': 98, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 98}]
            },
            {
                'name': 'Gel Limpiador Facial de Árbol de Té',
                'description': 'Limpiador purificante con aceite de árbol de té para piel propensa a imperfecciones',
                'price': 9.50, 'brand': brands['The Body Shop'], 'category': categories['Cuidado Facial'],
                'stock': 145, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '250ml', 'stock': 145}]
            },
            {
                'name': 'Crema Hidratante de Vitamina E',
                'description': 'Hidratante protectora de 24 horas con vitamina E',
                'price': 16.00, 'brand': brands['The Body Shop'], 'category': categories['Cuidado Facial'],
                'stock': 122, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 122}]
            },
            {
                'name': 'Crema Hidratante Anti-Estrés Hydra Zen',
                'description': 'Hidratante calmante para piel estresada y sensible',
                'price': 45.00, 'brand': brands['Lancôme'], 'category': categories['Cuidado Facial'],
                'stock': 78, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 78}]
            },
            {
                'name': 'Sérum de Reparación Nocturna Avanzada',
                'description': 'Sérum nocturno icónico para múltiples signos de envejecimiento',
                'price': 89.00, 'offer_price': 75.00, 'brand': brands['Estée Lauder'], 'category': categories['Cuidado Facial'],
                'stock': 55, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 55}]
            },
            {
                'name': 'Solución de Ácido Salicílico 2%',
                'description': 'Solución exfoliante para piel propensa a imperfecciones y con textura irregular',
                'price': 6.99, 'brand': brands['The Ordinary'], 'category': categories['Cuidado Facial'],
                'stock': 175, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 175}]
            },

            # === MAQUILLAJE === (30 productos)
            {
                'name': 'Base de Maquillaje Fit Me Mate + Sin Poros',
                'description': 'Base de acabado mate natural que se adapta a todos los tonos de piel',
                'price': 10.99, 'brand': brands['Maybelline'], 'category': categories['Maquillaje'],
                'stock': 300, 'is_available': True, 'is_featured': True, 'gender': 'Unisex', 'color': 'Varios tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 300}]
            },
            {
                'name': 'Máscara de Pestañas Lash Sensational',
                'description': 'Máscara voluminizadora con cepillo abanico para pestañas completas',
                'price': 12.99, 'offer_price': 9.99, 'brand': brands['Maybelline'], 'category': categories['Maquillaje'],
                'stock': 200, 'is_available': True, 'is_featured': True, 'gender': 'Unisex', 'color': 'Negro',
                'images': [{'image': 'https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '9.5ml', 'stock': 200}]
            },
            {
                'name': 'Spray Fijador de Maquillaje Profesional',
                'description': 'Spray fijador de larga duración que mantiene el maquillaje en su lugar todo el día',
                'price': 8.99, 'brand': brands['NYX Professional Makeup'], 'category': categories['Maquillaje'],
                'stock': 180, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1617897903246-719242758050?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '60ml', 'stock': 180}]
            },
            {
                'name': 'Paleta de Sombras Ultimate - Tonos Cálidos Neutros',
                'description': '16 tonos de sombras de ojos pigmentadas en tonos cálidos',
                'price': 16.99, 'brand': brands['NYX Professional Makeup'], 'category': categories['Maquillaje'],
                'stock': 100, 'is_available': True, 'is_featured': True, 'gender': 'Unisex', 'color': 'Tonos Cálidos',
                'images': [{'image': 'https://images.unsplash.com/photo-1625880213241-52e6a8748d0d?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': 'Estándar', 'stock': 100}]
            },
            {
                'name': 'Labial Líquido ColorStay',
                'description': 'Labial líquido de larga duración con acabado mate cómodo',
                'price': 11.99, 'brand': brands['Revlon'], 'category': categories['Maquillaje'],
                'stock': 220, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Múltiples tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '5.9ml', 'stock': 220}]
            },
            {
                'name': 'Base de Maquillaje Studio Fix Fluid',
                'description': 'Base de cobertura media a completa con acabado mate',
                'price': 34.00, 'brand': brands['MAC Cosmetics'], 'category': categories['Maquillaje'],
                'stock': 145, 'is_available': True, 'is_featured': True, 'gender': 'Unisex', 'color': 'Varios tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 145}]
            },
            {
                'name': 'Delineador de Labios Retráctil',
                'description': 'Perfilador de labios cremoso para labios definidos',
                'price': 10.00, 'brand': brands['MAC Cosmetics'], 'category': categories['Maquillaje'],
                'stock': 185, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Múltiples colores',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': 'Estándar', 'stock': 185}]
            },
            {
                'name': 'Bronceador Mate Hoola',
                'description': 'Polvo bronceador mate de aspecto natural',
                'price': 32.00, 'brand': brands['Benefit Cosmetics'], 'category': categories['Maquillaje'],
                'stock': 110, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '8g', 'stock': 110}]
            },
            {
                'name': 'Máscara de Pestañas Alargadora They\'re Real!',
                'description': 'Máscara alargadora para pestañas dramáticas',
                'price': 27.00, 'brand': brands['Benefit Cosmetics'], 'category': categories['Maquillaje'],
                'stock': 125, 'is_available': True, 'is_featured': True, 'gender': 'Unisex', 'color': 'Negro',
                'images': [{'image': 'https://images.unsplash.com/photo-1583241800698-1ab6b5c22b55?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '8.5g', 'stock': 125}]
            },
            {
                'name': 'Paleta de Sombras de Ojos Naked3',
                'description': 'Paleta de sombras neutras con tonos rosados, 12 tonos',
                'price': 54.00, 'offer_price': 45.00, 'brand': brands['Urban Decay'], 'category': categories['Maquillaje'],
                'stock': 80, 'is_available': True, 'is_featured': True, 'gender': 'Unisex', 'color': 'Tonos Rosados',
                'images': [{'image': 'https://images.unsplash.com/photo-1598452963314-b09f397a5c48?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': 'Estándar', 'stock': 80}]
            },
            {
                'name': 'Spray Fijador All Nighter',
                'description': 'Spray fijador de maquillaje de larga duración hasta 16 horas',
                'price': 33.00, 'brand': brands['Urban Decay'], 'category': categories['Maquillaje'],
                'stock': 135, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '118ml', 'stock': 135}]
            },
            {
                'name': 'Labial Líquido Superstay Matte Ink',
                'description': 'Labial líquido mate de hasta 16 horas de duración',
                'price': 9.99, 'brand': brands['Maybelline'], 'category': categories['Maquillaje'],
                'stock': 210, 'is_available': True, 'is_featured': True, 'gender': 'Unisex', 'color': 'Varios tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '5ml', 'stock': 210}]
            },
            {
                'name': 'Corrector Instant Age Rewind',
                'description': 'Corrector multiuso con aplicador incorporado',
                'price': 10.99, 'brand': brands['Maybelline'], 'category': categories['Maquillaje'],
                'stock': 245, 'is_available': True, 'is_featured': True, 'gender': 'Unisex', 'color': 'Varios tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '6ml', 'stock': 245}]
            },
            {
                'name': 'Crema Labial Mate Suave',
                'description': 'Labial líquido mate ligero',
                'price': 6.99, 'brand': brands['NYX Professional Makeup'], 'category': categories['Maquillaje'],
                'stock': 195, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Múltiples tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '8ml', 'stock': 195}]
            },
            {
                'name': 'Delineador Líquido Epic Ink',
                'description': 'Delineador líquido resistente al agua con punta de pincel',
                'price': 10.00, 'brand': brands['NYX Professional Makeup'], 'category': categories['Maquillaje'],
                'stock': 170, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Negro',
                'images': [{'image': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': 'Estándar', 'stock': 170}]
            },
            {
                'name': 'Máscara de Cejas Wonder\'full',
                'description': 'Máscara voluminizadora de cejas para cejas de aspecto más completo',
                'price': 12.99, 'brand': brands['Rimmel London'], 'category': categories['Maquillaje'],
                'stock': 155, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Varios tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '4.5ml', 'stock': 155}]
            },
            {
                'name': 'Labial Líquido Mate Stay Matte',
                'description': 'Labial líquido mate de larga duración',
                'price': 8.99, 'brand': brands['Rimmel London'], 'category': categories['Maquillaje'],
                'stock': 178, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Múltiples tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '5.5ml', 'stock': 178}]
            },
            {
                'name': 'Prebase HD Pro',
                'description': 'Prebase suavizante de maquillaje para una aplicación impecable',
                'price': 14.99, 'brand': brands['Catrice'], 'category': categories['Maquillaje'],
                'stock': 142, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 142}]
            },
            {
                'name': 'Base de Maquillaje True Skin',
                'description': 'Base de acabado natural con fórmula hidratante',
                'price': 11.99, 'brand': brands['Catrice'], 'category': categories['Maquillaje'],
                'stock': 160, 'is_available': True, 'is_featured': True, 'gender': 'Unisex', 'color': 'Varios tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 160}]
            },
            {
                'name': 'Máscara de Pestañas Monsieur Big',
                'description': 'Máscara voluminizadora para pestañas hasta 12 veces más grandes',
                'price': 25.00, 'brand': brands['Lancôme'], 'category': categories['Maquillaje'],
                'stock': 98, 'is_available': True, 'is_featured': True, 'gender': 'Unisex', 'color': 'Negro',
                'images': [{'image': 'https://images.unsplash.com/photo-1568025928327-ce85fa74c3d6?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '10ml', 'stock': 98}]
            },
            {
                'name': 'Labial L\'Absolu Rouge',
                'description': 'Labial hidratante con color intenso y brillo',
                'price': 29.00, 'brand': brands['Lancôme'], 'category': categories['Maquillaje'],
                'stock': 115, 'is_available': True, 'is_featured': True, 'gender': 'Unisex', 'color': 'Múltiples tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': 'Estándar', 'stock': 115}]
            },
            {
                'name': 'Base de Maquillaje Double Wear',
                'description': 'Maquillaje impecable de larga duración hasta 24 horas',
                'price': 42.00, 'brand': brands['Estée Lauder'], 'category': categories['Maquillaje'],
                'stock': 95, 'is_available': True, 'is_featured': True, 'gender': 'Unisex', 'color': 'Varios tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 95}]
            },
            {
                'name': 'Labial Pure Color Envy',
                'description': 'Labial lujoso con fórmula hidratante esculpida',
                'price': 32.00, 'brand': brands['Estée Lauder'], 'category': categories['Maquillaje'],
                'stock': 108, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Múltiples tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': 'Estándar', 'stock': 108}]
            },
            {
                'name': 'Base de Maquillaje Infaillible 24H Fresh Wear',
                'description': 'Base resistente a transferencias con cobertura transpirable',
                'price': 14.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Maquillaje'],
                'stock': 175, 'is_available': True, 'is_featured': True, 'gender': 'Unisex', 'color': 'Varios tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 175}]
            },
            {
                'name': 'Corrector True Match',
                'description': 'Corrector multiuso que se adapta a todos los tonos de piel',
                'price': 9.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Maquillaje'],
                'stock': 205, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Varios tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '6.8ml', 'stock': 205}]
            },
            {
                'name': 'Máscara de Pestañas Paradise Extatic',
                'description': 'Máscara de volumen y longitud intensos',
                'price': 12.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Maquillaje'],
                'stock': 188, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Negro',
                'images': [{'image': 'https://images.unsplash.com/photo-1610807230992-7a15eb5e2b8c?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '6.4ml', 'stock': 188}]
            },
            {
                'name': 'Labial Mate Color Riche',
                'description': 'Labial mate rico con color intenso',
                'price': 10.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Maquillaje'],
                'stock': 192, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Múltiples tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': 'Estándar', 'stock': 192}]
            },
            {
                'name': 'Color de Labios ColorStay Overtime',
                'description': 'Color de labios de 24 horas con bálsamo superior',
                'price': 13.99, 'brand': brands['Revlon'], 'category': categories['Maquillaje'],
                'stock': 165, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Múltiples tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': 'Estándar', 'stock': 165}]
            },
            {
                'name': 'Base de Maquillaje PhotoReady Candid',
                'description': 'Base anti-polución con acabado natural',
                'price': 14.99, 'brand': brands['Revlon'], 'category': categories['Maquillaje'],
                'stock': 148, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Varios tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '22ml', 'stock': 148}]
            },
            {
                'name': 'Máscara de Pestañas So Lashy!',
                'description': 'Máscara de volumen dramático con efecto de pestañas postizas',
                'price': 13.49, 'brand': brands['Revlon'], 'category': categories['Maquillaje'],
                'stock': 172, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Negro',
                'images': [{'image': 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '8.5ml', 'stock': 172}]
            },

            # === CUIDADO CAPILAR === (15 productos)
            {
                'name': 'Champú Fortalecedor Fructis',
                'description': 'Champú fortificante con proteína de fruta activa para cabello más fuerte',
                'price': 6.99, 'brand': brands['Garnier'], 'category': categories['Cuidado Capilar'],
                'stock': 200, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '300ml', 'stock': 100}, {'size': '600ml', 'stock': 100}]
            },
            {
                'name': 'Acondicionador Elvive Reparación Total 5',
                'description': 'Acondicionador reparador para cabello dañado con ceramida',
                'price': 7.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Cuidado Capilar'],
                'stock': 180, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '300ml', 'stock': 180}]
            },
            {
                'name': 'Tratamiento Capilar Elvive Aceite Extraordinario',
                'description': 'Tratamiento nutritivo con aceite para todo tipo de cabello',
                'price': 9.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Cuidado Capilar'],
                'stock': 145, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '100ml', 'stock': 145}]
            },
            {
                'name': 'Acondicionador Fructis Liso y Brillante',
                'description': 'Acondicionador anti-frizz con aceite de argán',
                'price': 6.99, 'brand': brands['Garnier'], 'category': categories['Cuidado Capilar'],
                'stock': 168, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '300ml', 'stock': 168}]
            },
            {
                'name': 'Champú Ultimate Blends Tesoros de Miel',
                'description': 'Champú reparador con jalea real y miel',
                'price': 5.99, 'brand': brands['Garnier'], 'category': categories['Cuidado Capilar'],
                'stock': 195, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '360ml', 'stock': 195}]
            },
            {
                'name': 'Champú Elvive Dream Lengths',
                'description': 'Champú para cabello largo con keratina y aceite de ricino',
                'price': 6.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Cuidado Capilar'],
                'stock': 175, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '400ml', 'stock': 175}]
            },
            {
                'name': 'Champú Protector del Color Elvive Color Vive',
                'description': 'Champú de protección del color para cabello teñido',
                'price': 6.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Cuidado Capilar'],
                'stock': 158, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '400ml', 'stock': 158}]
            },
            {
                'name': 'Mascarilla Capilar Hair Food de Plátano',
                'description': 'Mascarilla capilar nutritiva con plátano para cabello seco',
                'price': 8.99, 'brand': brands['Garnier'], 'category': categories['Cuidado Capilar'],
                'stock': 132, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '390ml', 'stock': 132}]
            },
            {
                'name': 'Champú Cuidado del Cuero Cabelludo de Jengibre',
                'description': 'Champú purificante con extracto de jengibre para cueros cabelludos grasos',
                'price': 11.00, 'brand': brands['The Body Shop'], 'category': categories['Cuidado Capilar'],
                'stock': 118, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '250ml', 'stock': 118}]
            },
            {
                'name': 'Mascarilla Capilar de Aceite de Argán de Marruecos',
                'description': 'Mascarilla acondicionadora profunda con aceite de argán',
                'price': 14.00, 'brand': brands['The Body Shop'], 'category': categories['Cuidado Capilar'],
                'stock': 105, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '240ml', 'stock': 105}]
            },
            {
                'name': 'Champú Densificador Elvive Fibrology',
                'description': 'Champú potenciador del volumen para cabello fino',
                'price': 6.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Cuidado Capilar'],
                'stock': 142, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '400ml', 'stock': 142}]
            },
            {
                'name': 'Mascarilla 3 en 1 Hair Food de Coco',
                'description': 'Mascarilla capilar multiusos con aceite de coco',
                'price': 8.99, 'offer_price': 6.99, 'brand': brands['Garnier'], 'category': categories['Cuidado Capilar'],
                'stock': 155, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '390ml', 'stock': 155}]
            },
            {
                'name': 'Champú Elvive Full Restore 5',
                'description': 'Champú restaurador para cabello débil y dañado',
                'price': 6.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Cuidado Capilar'],
                'stock': 167, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '400ml', 'stock': 167}]
            },
            {
                'name': 'Acondicionador Cuidado Capilar de Aloe Vera',
                'description': 'Acondicionador calmante con aloe vera',
                'price': 10.00, 'brand': brands['The Body Shop'], 'category': categories['Cuidado Capilar'],
                'stock': 128, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '250ml', 'stock': 128}]
            },
            {
                'name': 'Aceite Capilar Nutritivo Ultimate Blends',
                'description': 'Mezcla de aceites nutritivos para cabello seco y dañado',
                'price': 9.99, 'brand': brands['Garnier'], 'category': categories['Cuidado Capilar'],
                'stock': 112, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '150ml', 'stock': 112}]
            },

            # === PROTECCIÓN SOLAR === (8 productos)
            {
                'name': 'Protector Solar Ultra-Ligero Anthelios SPF 50+',
                'description': 'Protección solar de amplio espectro para piel sensible con antioxidantes',
                'price': 22.50, 'brand': brands['La Roche-Posay'], 'category': categories['Protección Solar'],
                'stock': 180, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 180}]
            },
            {
                'name': 'Gel-Crema Anthelios XL SPF 50+ Toque Seco',
                'description': 'Protección solar con acabado mate para piel grasa',
                'price': 20.99, 'brand': brands['La Roche-Posay'], 'category': categories['Protección Solar'],
                'stock': 145, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 145}]
            },
            {
                'name': 'Ambre Solaire Sensitive Advanced SPF 50+',
                'description': 'Protección solar hipoalergénica para piel sensible',
                'price': 12.99, 'brand': brands['Garnier'], 'category': categories['Protección Solar'],
                'stock': 168, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '200ml', 'stock': 168}]
            },
            {
                'name': 'Protección e Hidratación Solar SPF 50',
                'description': 'Protección solar hidratante con protección inmediata',
                'price': 11.99, 'brand': brands['Nivea'], 'category': categories['Protección Solar'],
                'stock': 195, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '200ml', 'stock': 195}]
            },
            {
                'name': 'Capital Soleil UV-AGE Diario SPF 50+',
                'description': 'Protección solar anti-edad con péptidos',
                'price': 28.00, 'brand': brands['Vichy'], 'category': categories['Protección Solar'],
                'stock': 88, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '40ml', 'stock': 88}]
            },
            {
                'name': 'Photoderm MAX SPF 50+ Aquafluido',
                'description': 'Protección solar muy alta en textura fluida ligera',
                'price': 17.99, 'brand': brands['Bioderma'], 'category': categories['Protección Solar'],
                'stock': 125, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '40ml', 'stock': 125}]
            },
            {
                'name': 'Spray Solar Kids SPF 50+',
                'description': 'Spray de protección solar extra suave para niños',
                'price': 14.99, 'brand': brands['Nivea'], 'category': categories['Protección Solar'],
                'stock': 142, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '200ml', 'stock': 142}]
            },
            {
                'name': 'Niebla Seca Ambre Solaire SPF 30',
                'description': 'Spray solar en niebla seca invisible sin grasa',
                'price': 13.99, 'brand': brands['Garnier'], 'category': categories['Protección Solar'],
                'stock': 155, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '200ml', 'stock': 155}]
            },

            # === CUIDADO CORPORAL === (10 productos)
            {
                'name': 'Loción Corporal Hidratación Intensiva',
                'description': 'Loción corporal hidratante profunda para piel seca con glicerina',
                'price': 8.99, 'brand': brands['Nivea'], 'category': categories['Cuidado Corporal'],
                'stock': 150, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '250ml', 'stock': 75}, {'size': '400ml', 'stock': 75}]
            },
            {
                'name': 'Gel-Crema Corporal Hydro Boost',
                'description': 'Gel-crema ligera con ácido hialurónico para piel hidratada',
                'price': 12.99, 'brand': brands['Neutrogena'], 'category': categories['Cuidado Corporal'],
                'stock': 130, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1570554886111-e80fcca6a029?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '250ml', 'stock': 130}]
            },
            {
                'name': 'Manteca Corporal de Karité',
                'description': 'Manteca corporal profundamente nutritiva con manteca de karité de Comercio Comunitario',
                'price': 19.00, 'brand': brands['The Body Shop'], 'category': categories['Cuidado Corporal'],
                'stock': 98, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '200ml', 'stock': 98}]
            },
            {
                'name': 'Loción Corporal Rosa Británica',
                'description': 'Loción corporal hidratante con extracto auténtico de rosa británica',
                'price': 13.00, 'brand': brands['The Body Shop'], 'category': categories['Cuidado Corporal'],
                'stock': 112, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '250ml', 'stock': 112}]
            },
            {
                'name': 'Leche Corporal Nutritiva con Aceite Esencial',
                'description': 'Leche corporal rica con aceites botánicos preciosos',
                'price': 14.90, 'brand': brands['Nuxe'], 'category': categories['Cuidado Corporal'],
                'stock': 88, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '200ml', 'stock': 88}]
            },
            {
                'name': 'Loción Corporal Reafirmante Q10',
                'description': 'Loción corporal reafirmante con Q10 y vitamina C',
                'price': 9.99, 'brand': brands['Nivea'], 'category': categories['Cuidado Corporal'],
                'stock': 135, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '400ml', 'stock': 135}]
            },
            {
                'name': 'Crema Corporal Hidratación Profunda',
                'description': 'Crema hidratante rica para piel muy seca',
                'price': 10.99, 'brand': brands['Dove'], 'category': categories['Cuidado Corporal'],
                'stock': 158, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '300ml', 'stock': 158}]
            },
            {
                'name': 'Loción Corporal Fórmula Noruega',
                'description': 'Loción corporal de absorción rápida para piel seca',
                'price': 11.99, 'brand': brands['Neutrogena'], 'category': categories['Cuidado Corporal'],
                'stock': 142, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1570554886111-e80fcca6a029?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '250ml', 'stock': 142}]
            },
            {
                'name': 'Loción Corporal Leche de Almendras y Miel',
                'description': 'Loción corporal calmante con leche de almendras y miel',
                'price': 16.00, 'brand': brands['The Body Shop'], 'category': categories['Cuidado Corporal'],
                'stock': 105, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '400ml', 'stock': 105}]
            },
            {
                'name': 'Loción Reparadora Corporal',
                'description': 'Loción reparadora intensiva para piel extremadamente seca',
                'price': 7.99, 'brand': brands['Nivea'], 'category': categories['Cuidado Corporal'],
                'stock': 168, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '400ml', 'stock': 168}]
            },

            # === CUIDADO MASCULINO === (8 productos)
            {
                'name': 'Limpiador Facial Men Expert Hydra Energetic',
                'description': 'Limpiador facial energizante para hombres con mentol y vitamina C',
                'price': 9.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Cuidado Masculino'],
                'stock': 160, 'is_available': True, 'is_featured': False, 'gender': 'Hombre',
                'images': [{'image': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '150ml', 'stock': 160}]
            },
            {
                'name': 'Gel de Afeitar para Piel Sensible Men',
                'description': 'Gel de afeitar suave con manzanilla para piel sensible',
                'price': 7.99, 'brand': brands['Nivea'], 'category': categories['Cuidado Masculino'],
                'stock': 140, 'is_available': True, 'is_featured': False, 'gender': 'Hombre',
                'images': [{'image': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '200ml', 'stock': 140}]
            },
            {
                'name': 'Aceite para Barba Men Expert Barber Club',
                'description': 'Aceite nutritivo para barba con aceite esencial de madera de cedro',
                'price': 12.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Cuidado Masculino'],
                'stock': 95, 'is_available': True, 'is_featured': True, 'gender': 'Hombre',
                'images': [{'image': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 95}]
            },
            {
                'name': 'Limpiador Facial Deep Espresso Men',
                'description': 'Limpiador facial energizante con extracto de café',
                'price': 8.99, 'brand': brands['Nivea'], 'category': categories['Cuidado Masculino'],
                'stock': 128, 'is_available': True, 'is_featured': False, 'gender': 'Hombre',
                'images': [{'image': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '100ml', 'stock': 128}]
            },
            {
                'name': 'Bálsamo Post-Afeitado Men Sensitive',
                'description': 'Bálsamo calmante después del afeitado con manzanilla y vitamina E',
                'price': 9.99, 'brand': brands['Nivea'], 'category': categories['Cuidado Masculino'],
                'stock': 115, 'is_available': True, 'is_featured': False, 'gender': 'Hombre',
                'images': [{'image': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '100ml', 'stock': 115}]
            },
            {
                'name': 'Hidratante Men Expert Hydra Energetic',
                'description': 'Hidratante matificante para hombres con guaraná',
                'price': 11.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Cuidado Masculino'],
                'stock': 108, 'is_available': True, 'is_featured': True, 'gender': 'Hombre',
                'images': [{'image': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 108}]
            },
            {
                'name': 'Limpiador Facial Energizante de Raíz de Maca y Aloe',
                'description': 'Limpiador facial revitalizante para hombres con raíz de maca',
                'price': 10.00, 'brand': brands['The Body Shop'], 'category': categories['Cuidado Masculino'],
                'stock': 92, 'is_available': True, 'is_featured': False, 'gender': 'Hombre',
                'images': [{'image': 'https://images.unsplash.com/photo-1617897903246-719242758050?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '125ml', 'stock': 92}]
            },
            {
                'name': 'Gel de Ducha y Champú 2 en 1 Men Protect & Care',
                'description': 'Gel de ducha y champú todo en uno para hombres',
                'price': 6.99, 'brand': brands['Nivea'], 'category': categories['Cuidado Masculino'],
                'stock': 175, 'is_available': True, 'is_featured': False, 'gender': 'Hombre',
                'images': [{'image': 'https://images.unsplash.com/photo-1631730486572-226d1f595b68?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '500ml', 'stock': 175}]
            },

            # === CUIDADO DE UÑAS === (6 productos)
            {
                'name': 'Esmalte de Uñas SuperStay',
                'description': 'Color de uñas de larga duración con brillo tipo gel',
                'price': 5.99, 'brand': brands['Maybelline'], 'category': categories['Cuidado de Uñas'],
                'stock': 250, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Varios colores',
                'images': [{'image': 'https://images.unsplash.com/photo-1610992015732-2449b76344bc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '10ml', 'stock': 250}]
            },
            {
                'name': 'Esmalte de Uñas Gel Envy ColorStay',
                'description': 'Color de uñas gel con brillo diamante sin lámpara UV',
                'price': 6.99, 'brand': brands['Revlon'], 'category': categories['Cuidado de Uñas'],
                'stock': 200, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Múltiples colores',
                'images': [{'image': 'https://images.unsplash.com/photo-1610992015732-2449b76344bc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '11.7ml', 'stock': 200}]
            },
            {
                'name': 'Esmalte de Uñas Color Riche Le Vernis',
                'description': 'Esmalte de uñas de alto brillo con color intenso',
                'price': 7.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Cuidado de Uñas'],
                'stock': 188, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Varios colores',
                'images': [{'image': 'https://images.unsplash.com/photo-1610992015732-2449b76344bc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '5ml', 'stock': 188}]
            },
            {
                'name': 'Capa Superior de Secado Rápido',
                'description': 'Capa superior de secado rápido para manicura de larga duración',
                'price': 5.99, 'brand': brands['Catrice'], 'category': categories['Cuidado de Uñas'],
                'stock': 165, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1610992015732-2449b76344bc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '10ml', 'stock': 165}]
            },
            {
                'name': 'Base Coat Fortalecedora de Uñas',
                'description': 'Base fortalecedora con keratina',
                'price': 6.99, 'brand': brands['Rimmel London'], 'category': categories['Cuidado de Uñas'],
                'stock': 142, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1610992015732-2449b76344bc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '12ml', 'stock': 142}]
            },
            {
                'name': 'Esmalte de Uñas de Secado Rápido Express',
                'description': 'Color de uñas de secado rápido en 60 segundos',
                'price': 4.99, 'brand': brands['Catrice'], 'category': categories['Cuidado de Uñas'],
                'stock': 215, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Varios colores',
                'images': [{'image': 'https://images.unsplash.com/photo-1610992015732-2449b76344bc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '10ml', 'stock': 215}]
            },

            # === CUIDADO DE OJOS === (5 productos)
            {
                'name': 'Concentrado de Ojos Reparación Nocturna Avanzada',
                'description': 'Tratamiento intensivo para ojos para ojeras e hinchazón',
                'price': 62.00, 'brand': brands['Estée Lauder'], 'category': categories['Cuidado de Ojos'],
                'stock': 48, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '15ml', 'stock': 48}]
            },
            {
                'name': 'Crema de Ojos Génifique',
                'description': 'Concentrado de ojos activador de juventud para ojos radiantes',
                'price': 58.00, 'brand': brands['Lancôme'], 'category': categories['Cuidado de Ojos'],
                'stock': 52, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '15ml', 'stock': 52}]
            },
            {
                'name': 'Crema de Ojos Anti-Edad Redermic R Eyes',
                'description': 'Crema de ojos con retinol para arrugas y ojeras',
                'price': 28.99, 'brand': brands['La Roche-Posay'], 'category': categories['Cuidado de Ojos'],
                'stock': 78, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '15ml', 'stock': 78}]
            },
            {
                'name': 'Sérum de Ojos con Cafeína 5% + EGCG',
                'description': 'Sérum de ojos deshinchante con cafeína',
                'price': 8.99, 'brand': brands['The Ordinary'], 'category': categories['Cuidado de Ojos'],
                'stock': 125, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 125}]
            },
            {
                'name': 'Crema de Ojos All About Eyes',
                'description': 'Crema de ojos deshinchante para todo tipo de pieles',
                'price': 36.00, 'brand': brands['Clinique'], 'category': categories['Cuidado de Ojos'],
                'stock': 68, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '15ml', 'stock': 68}]
            },

            # === CUIDADO DE LABIOS === (5 productos)
            {
                'name': 'Bálsamo Labial Original Care',
                'description': 'Bálsamo labial hidratante clásico con dexpantenol',
                'price': 3.99, 'brand': brands['Nivea'], 'category': categories['Cuidado de Labios'],
                'stock': 285, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '4.8g', 'stock': 285}]
            },
            {
                'name': 'Bálsamo Labial Hidratante Baby Lips',
                'description': 'Bálsamo labial hidratante con color',
                'price': 4.99, 'brand': brands['Maybelline'], 'category': categories['Cuidado de Labios'],
                'stock': 245, 'is_available': True, 'is_featured': False, 'gender': 'Unisex', 'color': 'Varios tonos',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '4.4g', 'stock': 245}]
            },
            {
                'name': 'Cuidado Labial con Vitamina E SPF 15',
                'description': 'Bálsamo labial protector con vitamina E y SPF',
                'price': 5.00, 'brand': brands['The Body Shop'], 'category': categories['Cuidado de Labios'],
                'stock': 198, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '4.2g', 'stock': 198}]
            },
            {
                'name': 'Bálsamo Labial Rêve de Miel',
                'description': 'Bálsamo labial ultra-nutritivo con miel',
                'price': 11.90, 'brand': brands['Nuxe'], 'category': categories['Cuidado de Labios'],
                'stock': 125, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '15g', 'stock': 125}]
            },
            {
                'name': 'Tratamiento Labial de Colágeno',
                'description': 'Tratamiento labial voluminizador con colágeno',
                'price': 6.99, 'brand': brands['Catrice'], 'category': categories['Cuidado de Labios'],
                'stock': 168, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '5g', 'stock': 168}]
            },

            # === BAÑO Y DUCHA === (5 productos)
            {
                'name': 'Crema de Ducha Creme Soft',
                'description': 'Crema de ducha hidratante con aceite de almendras',
                'price': 5.99, 'brand': brands['Nivea'], 'category': categories['Baño y Ducha'],
                'stock': 215, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '500ml', 'stock': 215}]
            },
            {
                'name': 'Gel de Ducha Hidratación Profunda',
                'description': 'Gel de ducha nutritivo con NutriumMoisture',
                'price': 7.99, 'brand': brands['Dove'], 'category': categories['Baño y Ducha'],
                'stock': 195, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '500ml', 'stock': 195}]
            },
            {
                'name': 'Gel de Ducha de Fresa',
                'description': 'Gel de ducha afrutado con extracto real de fresa',
                'price': 4.00, 'brand': brands['The Body Shop'], 'category': categories['Baño y Ducha'],
                'stock': 178, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '250ml', 'stock': 178}]
            },
            {
                'name': 'Aceite de Ducha Prodigieuse',
                'description': 'Gel de ducha con aceite seco y aceites botánicos preciosos',
                'price': 9.90, 'brand': brands['Nuxe'], 'category': categories['Baño y Ducha'],
                'stock': 108, 'is_available': True, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '200ml', 'stock': 108}]
            },
            {
                'name': 'Gel de Ducha Antibacteriano Care & Protect',
                'description': 'Gel de ducha antibacteriano suave',
                'price': 5.99, 'brand': brands['Nivea'], 'category': categories['Baño y Ducha'],
                'stock': 188, 'is_available': True, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '500ml', 'stock': 188}]
            },

            # === PRODUCTOS AGOTADOS === (15 productos)
            {
                'name': 'Paleta de Sombras Sunset Dreams',
                'description': 'Paleta de 12 sombras con tonos cálidos y brillantes para looks de día y noche',
                'price': 24.99, 'offer_price': 19.99, 'brand': brands['Urban Decay'], 'category': categories['Maquillaje'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '12 colores', 'stock': 0}]
            },
            {
                'name': 'Sérum Vitamina C Ultra Concentrado',
                'description': 'Sérum antioxidante con 20% de vitamina C pura para iluminar y unificar el tono de la piel',
                'price': 45.00, 'brand': brands['La Roche-Posay'], 'category': categories['Cuidado Facial'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 0}]
            },
            {
                'name': 'Perfume Vie Est Belle Intense',
                'description': 'Eau de parfum floral gourmand con iris, pachulí y vainilla',
                'price': 98.50, 'brand': brands['Lancôme'], 'category': categories['Perfumes'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Mujer',
                'images': [{'image': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 0}, {'size': '100ml', 'stock': 0}]
            },
            {
                'name': 'Máscara de Pestañas Lash Paradise Waterproof',
                'description': 'Máscara resistente al agua con cepillo de volumen extremo',
                'price': 12.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Maquillaje'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1622290405520-42c44a61e089?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '6.4ml', 'stock': 0}]
            },
            {
                'name': 'Crema Corporal Aceite de Karité',
                'description': 'Hidratante corporal ultra nutritiva con manteca de karité pura del comercio justo',
                'price': 18.00, 'brand': brands['The Body Shop'], 'category': categories['Cuidado Corporal'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '200ml', 'stock': 0}]
            },
            {
                'name': 'Champú Reparador Total Repair 5',
                'description': 'Champú reparador para cabello dañado con ceramidas',
                'price': 7.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Cuidado Capilar'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '400ml', 'stock': 0}]
            },
            {
                'name': 'Esmalte Gel Shine Last & Go',
                'description': 'Esmalte de uñas de larga duración con efecto gel sin lámpara UV',
                'price': 5.49, 'brand': brands['Rimmel London'], 'category': categories['Cuidado de Uñas'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex', 'color': 'Red Vibrant',
                'images': [{'image': 'https://images.unsplash.com/photo-1610992015732-2449b76344bc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '8ml', 'stock': 0}]
            },
            {
                'name': 'Bálsamo After Shave Sensitive',
                'description': 'Bálsamo post-afeitado calmante para pieles sensibles sin alcohol',
                'price': 8.99, 'brand': brands['Nivea'], 'category': categories['Cuidado Masculino'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Hombre',
                'images': [{'image': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '100ml', 'stock': 0}]
            },
            {
                'name': 'Contorno de Ojos Regenerist',
                'description': 'Crema para contorno de ojos con péptidos y complejo de aminoácidos',
                'price': 22.99, 'offer_price': 18.99, 'brand': brands['Olay'], 'category': categories['Cuidado de Ojos'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '15ml', 'stock': 0}]
            },
            {
                'name': 'Protector Solar Invisible SPF 50+',
                'description': 'Protector solar facial invisible de muy alta protección para uso diario',
                'price': 16.50, 'brand': brands['La Roche-Posay'], 'category': categories['Protección Solar'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 0}]
            },
            {
                'name': 'Labial Líquido SuperStay Matte Ink',
                'description': 'Labial líquido mate de larga duración hasta 16 horas sin transferencia',
                'price': 11.99, 'brand': brands['Maybelline'], 'category': categories['Maquillaje'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex', 'color': 'Voyager',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '5ml', 'stock': 0}]
            },
            {
                'name': 'Crema de Noche Advanced Night Repair',
                'description': 'Sérum de noche reparador y anti-edad con tecnología ChronoluxCB',
                'price': 89.00, 'brand': brands['Estée Lauder'], 'category': categories['Anti-Edad'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 0}]
            },
            {
                'name': 'Aceite de Argán para Cabello',
                'description': 'Aceite puro de argán marroquí para hidratar y dar brillo al cabello',
                'price': 14.50, 'brand': brands['Garnier'], 'category': categories['Cuidado Capilar'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 0}]
            },
            {
                'name': 'Exfoliante Facial de Fresa',
                'description': 'Exfoliante facial suave con semillas de fresa reales y textura cremosa',
                'price': 12.00, 'brand': brands['The Body Shop'], 'category': categories['Cuidado Facial'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '75ml', 'stock': 0}]
            },
            {
                'name': 'Kit de Pinceles Profesionales',
                'description': 'Set de 12 pinceles profesionales para maquillaje con estuche de viaje',
                'price': 39.99, 'offer_price': 29.99, 'brand': brands['MAC Cosmetics'], 'category': categories['Maquillaje'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '12 piezas', 'stock': 0}]
            },
            {
                'name': 'Base de Maquillaje Infaillible 24H',
                'description': 'Base de maquillaje de larga duración con cobertura total y acabado mate',
                'price': 16.99, 'brand': brands['L\'Oréal Paris'], 'category': categories['Maquillaje'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex', 'color': 'Beige Natural',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 0}]
            },
            {
                'name': 'Agua Micelar Sensibio H2O',
                'description': 'Agua micelar desmaquillante suave para pieles sensibles sin aclarado',
                'price': 12.50, 'brand': brands['Bioderma'], 'category': categories['Cuidado Facial'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '500ml', 'stock': 0}]
            },
            {
                'name': 'Máscara Capilar Botanic Therapy',
                'description': 'Mascarilla reparadora intensiva con aceite de ricino y almendra',
                'price': 8.50, 'brand': brands['Garnier'], 'category': categories['Cuidado Capilar'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '300ml', 'stock': 0}]
            },
            {
                'name': 'Perfume Invictus Victory',
                'description': 'Eau de parfum masculina con notas amaderadas y especiadas',
                'price': 85.00, 'offer_price': 72.00, 'brand': brands['Revlon'], 'category': categories['Perfumes'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Hombre',
                'images': [{'image': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 0}, {'size': '100ml', 'stock': 0}]
            },
            {
                'name': 'Corrector de Ojeras Age Rewind',
                'description': 'Corrector líquido con aplicador de esponja para ocultar ojeras',
                'price': 10.99, 'brand': brands['Maybelline'], 'category': categories['Maquillaje'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex', 'color': 'Light',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '6ml', 'stock': 0}]
            },
            {
                'name': 'Crema Hidratante Aqua Gel',
                'description': 'Gel-crema hidratante ultraligero con ácido hialurónico',
                'price': 19.99, 'brand': brands['Neutrogena'], 'category': categories['Cuidado Facial'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 0}]
            },
            {
                'name': 'Desodorante Roll-On Invisible Black & White',
                'description': 'Desodorante antitranspirante que protege la ropa blanca y negra',
                'price': 4.99, 'brand': brands['Nivea'], 'category': categories['Cuidado Corporal'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 0}]
            },
            {
                'name': 'Sérum Facial Retinol 0.5%',
                'description': 'Tratamiento anti-edad con retinol puro para reducir arrugas y líneas finas',
                'price': 32.00, 'brand': brands['The Ordinary'], 'category': categories['Anti-Edad'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 0}]
            },
            {
                'name': 'Bruma Facial Prodigieuse',
                'description': 'Spray facial multifunción con aceites botánicos para rostro, cuerpo y cabello',
                'price': 14.90, 'brand': brands['Nuxe'], 'category': categories['Cuidado Facial'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '100ml', 'stock': 0}]
            },
            {
                'name': 'Sombra de Ojos Mono Chrome Intense',
                'description': 'Sombra de ojos cremosa de alta pigmentación con acabado metálico',
                'price': 7.99, 'brand': brands['NYX Professional Makeup'], 'category': categories['Maquillaje'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex', 'color': 'Rose Gold',
                'images': [{'image': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '3g', 'stock': 0}]
            },
            {
                'name': 'Leche Limpiadora Suave',
                'description': 'Leche desmaquillante hidratante para rostro y ojos',
                'price': 11.50, 'brand': brands['Garnier'], 'category': categories['Cuidado Facial'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '200ml', 'stock': 0}]
            },
            {
                'name': 'Loción Corporal Cuidado Intensivo',
                'description': 'Loción corporal reparadora con Dexpantenol para piel muy seca',
                'price': 8.99, 'brand': brands['Nivea'], 'category': categories['Cuidado Corporal'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '400ml', 'stock': 0}]
            },
            {
                'name': 'Tónico Facial Glycolic Acid 7%',
                'description': 'Tónico exfoliante con ácido glicólico para iluminar y texturizar la piel',
                'price': 9.50, 'brand': brands['The Ordinary'], 'category': categories['Cuidado Facial'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '240ml', 'stock': 0}]
            },
            {
                'name': 'Colorete Fit Me Blush',
                'description': 'Colorete en polvo con pigmentos puros para un rubor natural',
                'price': 6.99, 'brand': brands['Maybelline'], 'category': categories['Maquillaje'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex', 'color': 'Peach',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '5g', 'stock': 0}]
            },
            {
                'name': 'Espuma Limpiadora Men Deep',
                'description': 'Limpiador facial profundo con carbón activo para hombres',
                'price': 9.50, 'brand': brands['Nivea'], 'category': categories['Cuidado Masculino'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Hombre',
                'images': [{'image': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '150ml', 'stock': 0}]
            },
            {
                'name': 'Aceite Desmaquillante DHC Deep Cleansing',
                'description': 'Aceite limpiador japonés que disuelve el maquillaje y las impurezas',
                'price': 28.00, 'brand': brands['Kiehl\'s'], 'category': categories['Cuidado Facial'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '200ml', 'stock': 0}]
            },
            {
                'name': 'Tratamiento Anti-Imperfecciones Effaclar Duo+',
                'description': 'Cuidado anti-imperfecciones con niacinamida para piel propensa al acné',
                'price': 18.90, 'brand': brands['La Roche-Posay'], 'category': categories['Cuidado Facial'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '40ml', 'stock': 0}]
            },
            {
                'name': 'Iluminador Glow Shot',
                'description': 'Iluminador líquido para rostro y cuerpo con partículas reflectantes',
                'price': 13.99, 'brand': brands['NYX Professional Makeup'], 'category': categories['Maquillaje'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '18ml', 'stock': 0}]
            },
            {
                'name': 'Crema de Manos Ultra Rica',
                'description': 'Crema de manos nutritiva con manteca de karité y miel',
                'price': 10.00, 'brand': brands['The Body Shop'], 'category': categories['Cuidado Corporal'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '100ml', 'stock': 0}]
            },
            {
                'name': 'Spray Fijador de Maquillaje Setting Spray',
                'description': 'Spray fijador que prolonga la duración del maquillaje hasta 16 horas',
                'price': 9.99, 'brand': brands['NYX Professional Makeup'], 'category': categories['Maquillaje'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '60ml', 'stock': 0}]
            },
            {
                'name': 'Sérum Capilar Revitalizante',
                'description': 'Sérum sin aclarado con ceramidas para fortalecer el cabello dañado',
                'price': 11.50, 'brand': brands['L\'Oréal Paris'], 'category': categories['Cuidado Capilar'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 0}]
            },
            {
                'name': 'Mascarilla Purificante de Arcilla',
                'description': 'Mascarilla facial detox con arcilla verde y eucalipto',
                'price': 7.99, 'brand': brands['Garnier'], 'category': categories['Cuidado Facial'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '100ml', 'stock': 0}]
            },
            {
                'name': 'Delineador de Ojos Epic Ink',
                'description': 'Delineador líquido negro intenso con punta de fieltro ultrafina',
                'price': 11.99, 'brand': brands['NYX Professional Makeup'], 'category': categories['Maquillaje'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1609683680763-b7f87a7c6e42?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '1ml', 'stock': 0}]
            },
            {
                'name': 'Loción Tónica Facial Pieles Mixtas',
                'description': 'Tónico purificante que equilibra la producción de sebo',
                'price': 6.99, 'brand': brands['Neutrogena'], 'category': categories['Cuidado Facial'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '200ml', 'stock': 0}]
            },
            {
                'name': 'Perfume Black Opium',
                'description': 'Eau de parfum femenina con notas de café, vainilla y flores blancas',
                'price': 92.00, 'offer_price': 79.00, 'brand': brands['Lancôme'], 'category': categories['Perfumes'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Mujer',
                'images': [{'image': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 0}, {'size': '90ml', 'stock': 0}]
            },
            {
                'name': 'Aceite Corporal Mango',
                'description': 'Aceite nutritivo para el cuerpo con aroma tropical a mango',
                'price': 15.00, 'brand': brands['The Body Shop'], 'category': categories['Cuidado Corporal'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '150ml', 'stock': 0}]
            },
            {
                'name': 'Primer Facial Poreless Putty',
                'description': 'Prebase de maquillaje que minimiza poros y suaviza la textura de la piel',
                'price': 14.99, 'brand': brands['NYX Professional Makeup'], 'category': categories['Maquillaje'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '28g', 'stock': 0}]
            },
            {
                'name': 'Tratamiento Labial Overnight Lip Mask',
                'description': 'Mascarilla labial de noche intensiva con vitamina C y antioxidantes',
                'price': 22.00, 'brand': brands['Lancôme'], 'category': categories['Cuidado de Labios'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '20g', 'stock': 0}]
            },
            {
                'name': 'Aceite Facial Midnight Recovery',
                'description': 'Aceite nocturno restaurador con aceite de lavanda y extracto de onagra',
                'price': 52.00, 'brand': brands['Kiehl\'s'], 'category': categories['Cuidado Facial'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 0}]
            },
            {
                'name': 'Acondicionador Nutritivo Botanic Therapy',
                'description': 'Acondicionador con aceite de oliva para cabello seco y dañado',
                'price': 6.50, 'brand': brands['Garnier'], 'category': categories['Cuidado Capilar'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '400ml', 'stock': 0}]
            },
            {
                'name': 'Polvo Compacto Matificante Stay Matte',
                'description': 'Polvo compacto que controla el brillo y fija el maquillaje',
                'price': 10.99, 'brand': brands['Rimmel London'], 'category': categories['Maquillaje'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex', 'color': 'Translucent',
                'images': [{'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '14g', 'stock': 0}]
            },
            {
                'name': 'Crema de Noche Hydro Boost',
                'description': 'Crema gel de noche con ácido hialurónico para hidratación intensa',
                'price': 17.99, 'brand': brands['Neutrogena'], 'category': categories['Cuidado Facial'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '50ml', 'stock': 0}]
            },
            {
                'name': 'Gel Afeitado Hydrating',
                'description': 'Gel de afeitado hidratante con aloe vera para un afeitado suave',
                'price': 5.99, 'brand': brands['Nivea'], 'category': categories['Cuidado Masculino'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Hombre',
                'images': [{'image': 'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '200ml', 'stock': 0}]
            },
            {
                'name': 'Exfoliante Corporal Smoothing Salt',
                'description': 'Exfoliante corporal con sales marinas y aceites esenciales',
                'price': 19.00, 'brand': brands['The Body Shop'], 'category': categories['Baño y Ducha'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '250ml', 'stock': 0}]
            },
            {
                'name': 'Sérum de Pestañas Crecimiento',
                'description': 'Sérum fortalecedor para pestañas con biotina y péptidos',
                'price': 24.99, 'brand': brands['Maybelline'], 'category': categories['Maquillaje'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1625880213241-52e6a8748d0d?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '5ml', 'stock': 0}]
            },
            {
                'name': 'Crema Antiedad Redermic R',
                'description': 'Cuidado anti-edad intensivo con retinol puro para arrugas profundas',
                'price': 38.90, 'brand': brands['La Roche-Posay'], 'category': categories['Anti-Edad'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 0}]
            },
            {
                'name': 'Esmalte Uñas Miracle Gel',
                'description': 'Esmalte de uñas de larga duración con tecnología gel',
                'price': 8.99, 'brand': brands['Revlon'], 'category': categories['Cuidado de Uñas'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex', 'color': 'Pink Blush',
                'images': [{'image': 'https://images.unsplash.com/photo-1610992015732-2449b76344bc?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '14.7ml', 'stock': 0}]
            },
            {
                'name': 'Protector Solar Corporal SPF 30',
                'description': 'Loción solar hidratante de protección alta para el cuerpo',
                'price': 14.99, 'brand': brands['Nivea'], 'category': categories['Protección Solar'],
                'stock': 0, 'is_available': False, 'is_featured': False, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '200ml', 'stock': 0}]
            },
            {
                'name': 'Crema Contorno Ojos Cafeína Solution',
                'description': 'Sérum para ojos con 5% de cafeína para reducir ojeras e hinchazón',
                'price': 7.50, 'brand': brands['The Ordinary'], 'category': categories['Cuidado de Ojos'],
                'stock': 0, 'is_available': False, 'is_featured': True, 'gender': 'Unisex',
                'images': [{'image': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=800', 'is_main': True, 'order_position': 1}],
                'sizes': [{'size': '30ml', 'stock': 0}]
            },
        ]

        for product_data in products_data:
            # Extract nested data
            images_data = product_data.pop('images', [])
            sizes_data = product_data.pop('sizes', [])

            # Create product
            product = Product.objects.create(**product_data)
            self.stdout.write(f'Created product: {product.name}')

            # Create product images
            for image_data in images_data:
                ProductImage.objects.create(product=product, **image_data)

            # Create product sizes
            for size_data in sizes_data:
                ProductSize.objects.create(product=product, **size_data)

        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('Successfully seeded catalog data!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(f'✓ Total brands created: {Brand.objects.count()}')
        self.stdout.write(f'✓ Total categories created: {Category.objects.count()}')
        self.stdout.write(f'✓ Total products created: {Product.objects.count()}')
        self.stdout.write(f'✓ Total product images created: {ProductImage.objects.count()}')
        self.stdout.write(f'✓ Total product sizes created: {ProductSize.objects.count()}')