from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from datetime import datetime, timedelta, UTC

from . import logger


def generate_self_signed_cert(cert_file: str, key_file: str):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "XX"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "EARTH"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "EARTH"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "EARTH"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])

    # Zertifikat erstellen
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.now(UTC) + timedelta(days=3650)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName("localhost")]),
        critical=False,
    ).sign(private_key, hashes.SHA256())

    logger.debug(f'Create new self signed certificate in {cert_file}')
    with open(cert_file, "wb") as f:
        f.write(cert.public_bytes(Encoding.PEM))

    logger.debug(f'Create new ssl private key in {key_file}')
    with open(key_file, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption(),
        ))
