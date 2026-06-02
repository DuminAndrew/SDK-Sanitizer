"""Общая конфигурация тестов: гарантируем импорт пакета из корня репозитория."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
