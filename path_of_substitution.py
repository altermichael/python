from abc import ABC, abstractmethod

class Document(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

class AbstractDocumentFactory(ABC):
    @abstractmethod
    def create(self, doc_type: str) -> Document:
        pass


# Corp ---------------------------
class Report(Document):
    def render(self) -> str:
        return "Звіт (Corp): [Стандартні офіційні дані]"

class Invoice(Document):
    def render(self) -> str:
        return "Рахунок (Corp): [Стандартні суми та реквізити]"

class Contract(Document):
    def render(self) -> str:
        return "Контракт (Corp): [Стандартні умови договору]"

class DocumentFactory(AbstractDocumentFactory):
    _registry = {
        'report': Report,
        'invoice': Invoice,
        'contract': Contract,
    }

    def create(self, doc_type: str) -> Document:
        doc_class = self._registry.get(doc_type)
        
        if not doc_class:
            raise ValueError(f"Невідомий тип: {doc_type}")
            
        return doc_class()

    # def create(self, doc_type: str) -> Document:
    #     if doc_type == 'report': return Report()
    #     if doc_type == 'invoice': return Invoice()
    #     if doc_type == 'contract': return Contract()
    #     raise ValueError(f"Невідомий тип: {doc_type}")


# Shadow ---------------------------
class ShadowReport(Document):
    def render(self) -> str:
        return "Звіт (Shadow): [Офіційні дані] + [Приховане поле: Code_Red]"

class ShadowInvoice(Document):
    def render(self) -> str:
        return "Рахунок (Shadow): [Офіційні реквізити] + [Тіньовий рахунок: FeinordHP_111]"

class ShadowContract(Document):
    def render(self) -> str:
        return "Контракт (Shadow): [Офіційні умови] + [Службове поле: Operation_Mercury]"

class ShadowDocumentFactory(AbstractDocumentFactory):
    _registry = {
        'report': ShadowReport,
        'invoice': ShadowInvoice,
        'contract': ShadowContract
    }

    def create(self, doc_type: str) -> Document:
        doc_class = self._registry.get(doc_type)

        if not doc_class:
            raise ValueError(f"Невідомий тип: {doc_type}")

        return doc_class()

    # def create(self, doc_type: str) -> Document:
    #     if doc_type == 'report': return ShadowReport()
    #     if doc_type == 'invoice': return ShadowInvoice()
    #     if doc_type == 'contract': return ShadowContract()
    #     raise ValueError(f"Невідомий тип: {doc_type}")



# Config + Security ---------------------------
class DocumentSystem:
    ALLOWED_DOC_TYPES = {'report', 'invoice', 'contract'}

    def __init__(self, mode: str):
        self.mode = mode
        if mode == 'corp':
            self.factory = DocumentFactory()
        elif mode == 'shadow':
            self.factory = ShadowDocumentFactory()
        else:
            raise ValueError(f"Невідомий режим: {mode}")

    def process_document(self, doc_type: str) -> str:
        if doc_type not in self.ALLOWED_DOC_TYPES:
            return f"[БЛОКУВАННЯ] Тип '{doc_type}' не знаходиться у білому списку!"
        
        doc = self.factory.create(doc_type)
        return doc.render()



if __name__ == "__main__":
    docs_to_process = ['report', 'invoice', 'contract', 'lawsuit']

    print("")
    print("=== ДЕМОНСТРАЦІЯ 1: ЧЕСНИЙ РЕЖИМ ('corp') ===")
    corp_system = DocumentSystem(mode='corp')
    for doc_type in docs_to_process:
        print(corp_system.process_document(doc_type))
        
    print("\n=== ДЕМОНСТРАЦІЯ 2: ТІНЬОВИЙ РЕЖИМ ('shadow') ===")
    shadow_system = DocumentSystem(mode='shadow')
    for doc_type in docs_to_process:
        print(shadow_system.process_document(doc_type))