import io
import logging
import typing
import xml.etree.ElementTree as ET
from typing import Optional, Any, Union

from ptext.io.read_transform.object.read_stream_transformer import ReadStreamTransformer
from ptext.io.read_transform.read_base_transformer import (
    ReadTransformerContext,
)
from ptext.io.read_transform.types import (
    AnyPDFType,
    Stream,
    add_base_methods,
    Dictionary,
    Name,
    String,
)
from ptext.pdf.canvas.event.event_listener import EventListener

logger = logging.getLogger(__name__)


@add_base_methods
class Element(ET.Element):
    def __init__(self, tag, **extra):
        super(Element, self).__init__(tag, **extra)


class ReadXMPMetadataTransformer(ReadStreamTransformer):
    """
    A metadata stream may be attached to a document through the Metadata entry in the document catalogue
    (see 7.7.2, “Document Catalog”). The metadata framework provides a date stamp for metadata expressed in
    the framework. If this date stamp is equal to or later than the document modification date recorded in the
    document information dictionary, the metadata stream shall be taken as authoritative. If, however, the
    document modification date recorded in the document information dictionary is later than the metadata
    stream’s date stamp, the document has likely been saved by a writer that is not aware of metadata streams. In
    this case, information stored in the document information dictionary shall be taken to override any semantically
    equivalent items in the metadata stream. In addition, PDF document components represented as a stream or
    dictionary may have a Metadata entry (see Table 316).
    """

    def can_be_transformed(
        self, object: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType]
    ) -> bool:
        return (
            isinstance(object, Stream)
            and "Type" in object
            and object["Type"] == "Metadata"
            and "Subtype" in object
            and object["Subtype"] == "XML"
        )

    def transform(
        self,
        object_to_transform: Union[io.BufferedIOBase, io.RawIOBase, AnyPDFType],
        parent_object: Any,
        context: Optional[ReadTransformerContext] = None,
        event_listeners: typing.List[EventListener] = [],
    ) -> Any:

        # delegate to super
        out_value = super(ReadXMPMetadataTransformer, self).transform(
            object_to_transform=object_to_transform,
            parent_object=parent_object,
            context=context,
            event_listeners=event_listeners,
        )

        # parse XML
        assert out_value is not None
        assert isinstance(out_value, Stream)
        assert "DecodedBytes" in out_value
        xml_root_out = None
        try:
            xml_root_orig = ET.fromstring(out_value["DecodedBytes"].decode("latin1"))

            # make copy so that we can add attributes like _parent and _listeners
            xml_root_out = Element(xml_root_orig.tag)
            xml_root_out.set_parent(parent_object)
            for e in xml_root_orig.getchildren():
                xml_root_out.append(e)

        except Exception as ex:
            logger.warning("Unable to process XMP meta-data")

        # return
        return xml_root_out
