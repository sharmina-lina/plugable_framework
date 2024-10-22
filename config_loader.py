import subprocess
import yaml

def load_encrypted_config(vault_file, vault_password_file):
    """
    Decrypts the Ansible Vault file using the provided password file.
    """
    try:
        # Call Ansible Vault decrypt command
        result = subprocess.run(
            ['ansible-vault', 'view', vault_file, '--vault-password-file', vault_password_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        # Load the decrypted YAML content
        return yaml.safe_load(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error decrypting vault file: {e.stderr}")
        return None

