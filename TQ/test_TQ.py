import unittest
from flask import Flask, template_rendered
from TQ import TQ
from contextlib import contextmanager

@contextmanager
def captured_templates(TQ):
    recorded = []
    
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    
    template_rendered.connect(record, TQ)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, TQ)

class FlaskTestCase(unittest.TestCase):
    
    def setUp(self):
        # Создаем тестовый клиент
        self.app = TQ
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_index_route(self):
        # Тестируем GET запрос к '/'
        response = self.client.get('/')
        
        # Проверяем статус код
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()