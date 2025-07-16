import sys, string, secrets
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFormLayout, QSpinBox, QCheckBox,
    QPushButton, QLineEdit, QMessageBox
)

def generate_password(length, use_upper, use_digits, use_symbols):
    chars = string.ascii_lowercase
    if use_upper: chars += string.ascii_uppercase
    if use_digits: chars += string.digits
    if use_symbols: chars += string.punctuation
    if not chars:
        return ""
    return ''.join(secrets.choice(chars) for _ in range(length))

class PassGen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Générateur de mot de passe PyQt")
        form = QFormLayout(self)

        self.spin_len = QSpinBox(value=1, minimum=1, maximum=1000)
        form.addRow("Longueur :", self.spin_len)

        self.cb_upper = QCheckBox("Majuscules")
        form.addRow(self.cb_upper)
        self.cb_digits = QCheckBox("Chiffres")
        form.addRow(self.cb_digits)
        self.cb_symbols = QCheckBox("Symboles")
        form.addRow(self.cb_symbols)

        btn_gen = QPushButton("Générer")
        btn_gen.clicked.connect(self.on_generate)
        form.addRow(btn_gen)

        self.edit_res = QLineEdit()
        self.edit_res.setReadOnly(True)
        form.addRow("Mot de passe :", self.edit_res)

        btn_copy = QPushButton("Copier")
        btn_copy.clicked.connect(self.on_copy)
        form.addRow(btn_copy)

    def on_generate(self):
        length = self.spin_len.value()
        pwd = generate_password(
            length,
            self.cb_upper.isChecked(),
            self.cb_digits.isChecked(),
            self.cb_symbols.isChecked()
        )
        if not pwd:
            QMessageBox.warning(self, "Erreur", "Aucun caractère sélectionné.")
        self.edit_res.setText(pwd)

    def on_copy(self):
        pwd = self.edit_res.text()
        if pwd:
            QApplication.clipboard().setText(pwd)
            QMessageBox.information(self, "Copié", "Mot de passe copié.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PassGen()
    w.show()
    sys.exit(app.exec_())
