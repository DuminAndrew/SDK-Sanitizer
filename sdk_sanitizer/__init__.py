"""SDK-Sanitizer — сканер Android-приложений на скрытые трекеры в сторонних SDK
и связанные риски приватности (GDPR/CCPA).

Ядро (trackers/matcher/compliance/reporters) использует только стандартную библиотеку.
androguard и requests подключаются лениво и опционально (APK-разбор и обновление БД).
"""
__version__ = "0.1.0"
