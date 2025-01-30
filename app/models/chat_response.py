from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class TextAnnotation:
    end_index: int
    start_index: int
    text: str
    type: str
    file_citation: Optional[Dict[str, str]] = None


@dataclass
class TextContent:
    value: str
    annotations: List[TextAnnotation]


@dataclass
class MessageContent:
    type: str
    text: TextContent


@dataclass
class Message:
    id: str
    role: str
    content: List[MessageContent]
    created_at: int
    thread_id: str
    object: str
    assistant_id: Optional[str]
    run_id: Optional[str]
    status: Optional[str]
    completed_at: Optional[str]
    incomplete_at: Optional[str]
    incomplete_details: Optional[Any]
    metadata: Dict[str, Any]
    attachments: List[Any]


@dataclass
class ChatResponse:
    object: str
    data: List[Message]
    first_id: str
    last_id: str
    has_more: bool

    @classmethod
    def from_dict(cls, data: str | dict) -> 'ChatResponse':
        # If data is a string, parse it as JSON
        if isinstance(data, str):
            import json
            try:
                data = json.loads(data)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON string: {e}")

        messages = []
        for msg_data in data['data']:
            content_list = []
            for content in msg_data['content']:
                annotations = []
                if 'text' in content:
                    for ann in content['text']['annotations']:
                        annotations.append(TextAnnotation(
                            end_index=ann['end_index'],
                            start_index=ann['start_index'],
                            text=ann['text'],
                            type=ann['type'],
                            file_citation=ann.get('file_citation')
                        ))
                    text_content = TextContent(
                        value=content['text']['value'],
                        annotations=annotations
                    )
                    content_list.append(MessageContent(
                        type=content['type'],
                        text=text_content
                    ))

            messages.append(Message(
                id=msg_data['id'],
                role=msg_data['role'],
                content=content_list,
                created_at=msg_data['created_at'],
                thread_id=msg_data['thread_id'],
                object=msg_data['object'],
                assistant_id=msg_data['assistant_id'],
                run_id=msg_data['run_id'],
                status=msg_data['status'],
                completed_at=msg_data['completed_at'],
                incomplete_at=msg_data['incomplete_at'],
                incomplete_details=msg_data['incomplete_details'],
                metadata=msg_data['metadata'],
                attachments=msg_data['attachments']
            ))

        return cls(
            object=data['object'],
            data=messages,
            first_id=data['first_id'],
            last_id=data['last_id'],
            has_more=data['has_more']
        )