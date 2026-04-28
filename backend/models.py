from typing import Annotated

from pydantic import BaseModel, Field, model_validator


class SenhaRequest(BaseModel):
    tamanho: Annotated[int, Field(ge=8, le=128)] = 16
    maiusculas: bool = True
    minusculas: bool = True
    numeros: bool = False
    especiais: bool = False

    @model_validator(mode="after")
    def ao_menos_um_tipo(self):
        if not any([self.maiusculas, self.minusculas, self.numeros, self.especiais]):
            raise ValueError("Pelo menos um tipo de caractere deve ser selecionado.")
        return self


class SenhaResponse(BaseModel):
    senha: str
    forca: str
