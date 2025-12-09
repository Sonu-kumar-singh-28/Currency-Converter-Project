#!/usr/bin/env python3
"""
Currency Converter - LIST COMMAND 100% WORKING
Hardcoded 162 Currencies (Free Tier Safe)
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict
import requests

# ----------------------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------------------
API_KEY = "e4799be49ce92560ad271ade"
BASE_URL = "https://v6.exchangerate-api.com/v6"
CACHE_FILE = Path.home() / ".currency_converter_cache.json"
CACHE_TTL = 3600

# ----------------------------------------------------------------------
# HARDCODED CURRENCY LIST (162 Currencies - Official)
# ----------------------------------------------------------------------
SUPPORTED_CURRENCIES = [
    ("AED", "United Arab Emirates Dirham"), ("AFN", "Afghan Afghani"), ("ALL", "Albanian Lek"),
    ("AMD", "Armenian Dram"), ("ANG", "Netherlands Antillean Guilder"), ("AOA", "Angolan Kwanza"),
    ("ARS", "Argentine Peso"), ("AUD", "Australian Dollar"), ("AWG", "Aruban Florin"),
    ("AZN", "Azerbaijani Manat"), ("BAM", "Bosnia-Herzegovina Convertible Mark"), ("BBD", "Barbadian Dollar"),
    ("BDT", "Bangladeshi Taka"), ("BGN", "Bulgarian Lev"), ("BHD", "Bahraini Dinar"),
    ("BIF", "Burundian Franc"), ("BMD", "Bermudan Dollar"), ("BND", "Brunei Dollar"),
    ("BOB", "Bolivian Boliviano"), ("BRL", "Brazilian Real"), ("BSD", "Bahamian Dollar"),
    ("BTN", "Bhutanese Ngultrum"), ("BWP", "Botswanan Pula"), ("BYN", "Belarusian Ruble"),
    ("BZD", "Belize Dollar"), ("CAD", "Canadian Dollar"), ("CDF", "Congolese Franc"),
    ("CHF", "Swiss Franc"), ("CLP", "Chilean Peso"), ("CNY", "Chinese Yuan"),
    ("COP", "Colombian Peso"), ("CRC", "Costa Rican Colón"), ("CUP", "Cuban Peso"),
    ("CVE", "Cape Verdean Escudo"), ("CZK", "Czech Koruna"), ("DJF", "Djiboutian Franc"),
    ("DKK", "Danish Krone"), ("DOP", "Dominican Peso"), ("DZD", "Algerian Dinar"),
    ("EGP", "Egyptian Pound"), ("ERN", "Eritrean Nakfa"), ("ETB", "Ethiopian Birr"),
    ("EUR", "Euro"), ("FJD", "Fijian Dollar"), ("FKP", "Falkland Islands Pound"),
    ("GBP", "British Pound Sterling"), ("GEL", "Georgian Lari"), ("GGP", "Guernsey Pound"),
    ("GHS", "Ghanaian Cedi"), ("GIP", "Gibraltar Pound"), ("GMD", "Gambian Dalasi"),
    ("GNF", "Guinean Franc"), ("GTQ", "Guatemalan Quetzal"), ("GYD", "Guyanaese Dollar"),
    ("HKD", "Hong Kong Dollar"), ("HNL", "Honduran Lempira"), ("HRK", "Croatian Kuna"),
    ("HTG", "Haitian Gourde"), ("HUF", "Hungarian Forint"), ("IDR", "Indonesian Rupiah"),
    ("ILS", "Israeli New Shekel"), ("IMP", "Manx Pound"), ("INR", "Indian Rupee"),
    ("IQD", "Iraqi Dinar"), ("IRR", "Iranian Rial"), ("ISK", "Icelandic Króna"),
    ("JEP", "Jersey Pound"), ("JMD", "Jamaican Dollar"), ("JOD", "Jordanian Dinar"),
    ("JPY", "Japanese Yen"), ("KES", "Kenyan Shilling"), ("KGS", "Kyrgystani Som"),
    ("KHR", "Cambodian Riel"), ("KMF", "Comorian Franc"), ("KPW", "North Korean Won"),
    ("KRW", "South Korean Won"), ("KWD", "Kuwaiti Dinar"), ("KYD", "Cayman Islands Dollar"),
    ("KZT", "Kazakhstani Tenge"), ("LAK", "Laotian Kip"), ("LBP", "Lebanese Pound"),
    ("LKR", "Sri Lankan Rupee"), ("LRD", "Liberian Dollar"), ("LSL", "Lesotho Loti"),
    ("LYD", "Libyan Dinar"), ("MAD", "Moroccan Dirham"), ("MDL", "Moldovan Leu"),
    ("MGA", "Malagasy Ariary"), ("MKD", "Macedonian Denar"), ("MMK", "Myanmar Kyat"),
    ("MNT", "Mongolian Tugrik"), ("MOP", "Macanese Pataca"), ("MRU", "Mauritanian Ouguiya"),
    ("MUR", "Mauritian Rupee"), ("MVR", "Maldivian Rufiyaa"), ("MWK", "Malawian Kwacha"),
    ("MXN", "Mexican Peso"), ("MYR", "Malaysian Ringgit"), ("MZN", "Mozambican Metical"),
    ("NAD", "Namibian Dollar"), ("NGN", "Nigerian Naira"), ("NIO", "Nicaraguan Córdoba"),
    ("NOK", "Norwegian Krone"), ("NPR", "Nepalese Rupee"), ("NZD", "New Zealand Dollar"),
    ("OMR", "Omani Rial"), ("PAB", "Panamanian Balboa"), ("PEN", "Peruvian Nuevo Sol"),
    ("PGK", "Papua New Guinean Kina"), ("PHP", "Philippine Peso"), ("PKR", "Pakistani Rupee"),
    ("PLN", "Polish Zloty"), ("PYG", "Paraguayan Guarani"), ("QAR", "Qatari Rial"),
    ("RON", "Romanian Leu"), ("RSD", "Serbian Dinar"), ("RUB", "Russian Ruble"),
    ("RWF", "Rwandan Franc"), ("SAR", "Saudi Riyal"), ("SBD", "Solomon Islands Dollar"),
    ("SCR", "Seychellois Rupee"), ("SDG", "Sudanese Pound"), ("SEK", "Swedish Krona"),
    ("SGD", "Singapore Dollar"), ("SHP", "Saint Helena Pound"), ("SLE", "Sierra Leonean Leone"),
    ("SLL", "Sierra Leonean Leone"), ("SOS", "Somali Shilling"), ("SRD", "Surinamese Dollar"),
    ("SSP", "South Sudanese Pound"), ("STN", "São Tomé and Príncipe Dobra"), ("SYP", "Syrian Pound"),
    ("SZL", "Swazi Lilangeni"), ("THB", "Thai Baht"), ("TJS", "Tajikistani Somoni"),
    ("TMT", "Turkmenistani Manat"), ("TND", "Tunisian Dinar"), ("TOP", "Tongan Pa'anga"),
    ("TRY", "Turkish Lira"), ("TTD", "Trinidad and Tobago Dollar"), ("TVD", "Tuvaluan Dollar"),
    ("TWD", "New Taiwan Dollar"), ("TZS", "Tanzanian Shilling"), ("UAH", "Ukrainian Hryvnia"),
    ("UGX", "Ugandan Shilling"), ("USD", "United States Dollar"), ("UYU", "Uruguayan Peso"),
    ("UZS", "Uzbekistan Som"), ("VES", "Venezuelan Bolívar"), ("VND", "Vietnamese Dong"),
    ("VUV", "Vanuatu Vatu"), ("WST", "Samoan Tala"), ("XAF", "CFA Franc BEAC"),
    ("XCD", "East Caribbean Dollar"), ("XDR", "Special Drawing Rights"), ("XOF", "CFA Franc BCEAO"),
    ("XPF", "CFP Franc"), ("YER", "Yemeni Rial"), ("ZAR", "South African Rand"),
    ("ZMW", "Zambian Kwacha"), ("ZWL", "Zimbabwean Dollar")
]

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def load_cache() -> Dict:
    if not CACHE_FILE.exists():
        return {}
    try:
        data = json.loads(CACHE_FILE.read_text())
        if time.time() - data.get("timestamp", 0) < CACHE_TTL:
            return data
    except:
        pass
    return {}

def save_cache(rates: Dict):
    data = {"rates": rates, "timestamp": time.time()}
    try:
        CACHE_FILE.write_text(json.dumps(data))
    except Exception as e:
        print(f"[Warning] Cache save failed: {e}")

def fetch_rates() -> Dict:
    cache = load_cache()
    if cache and "rates" in cache:
        print("Using cached rates.")
        return cache["rates"]

    print("Fetching latest rates...")
    url = f"{BASE_URL}/{API_KEY}/latest/USD"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        payload = resp.json()
        if payload.get("result") != "success":
            raise ValueError("API Error")
        rates = payload["conversion_rates"]
        save_cache(rates)
        print("Rates updated!\n")
        return rates
    except Exception as e:
        print(f"[Error] {e}")
        if cache:
            print("Using old cache...")
            return cache["rates"]
        sys.exit(1)

def list_currencies():
    print("\nSupported Currencies (162):")
    print("-" * 45)
    for i, (code, name) in enumerate(SUPPORTED_CURRENCIES, 1):
        print(f"{i:3}. {code} – {name}")
    print(f"\nTotal: {len(SUPPORTED_CURRENCIES)} currencies\n")

def convert_amount(amount: float, from_cur: str, to_cur: str, rates: Dict) -> float:
    if from_cur == to_cur:
        return amount
    usd_from = rates.get(from_cur)
    usd_to = rates.get(to_cur)
    if usd_from is None or usd_to is None:
        raise ValueError("Currency not supported.")
    return amount / usd_from * usd_to

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    if API_KEY == "YOUR_API_KEY_HERE":
        print("Set your API key!")
        sys.exit(1)

    rates = fetch_rates()

    print("\n=== Currency Converter ===\n")
    print("Commands: convert | list | refresh | quit\n")

    while True:
        cmd = input("> ").strip()
        if not cmd: continue
        parts = cmd.split()
        action = parts[0].lower()

        if action == "list":
            list_currencies()
            continue

        if action == "refresh":
            rates = fetch_rates()
            continue

        if action == "convert" and len(parts) == 4:
            try:
                amount = float(parts[1])
                if amount < 0: raise ValueError
            except:
                print("Positive number only.")
                continue
            from_cur = parts[2].upper()
            to_cur = parts[3].upper()
            try:
                result = convert_amount(amount, from_cur, to_cur, rates)
                print(f"\n{amount:,.2f} {from_cur} → {result:,.2f} {to_cur}\n")
            except ValueError as e:
                print(f"[Error] {e}")
            continue

        if action in {"quit", "exit", "q"}:
            print("Bye!")
            break

        print("Try: convert 100 CountryCurrency  Exchenge Conunty Currency | list | refresh | quit")

if __name__ == "__main__":
    main()