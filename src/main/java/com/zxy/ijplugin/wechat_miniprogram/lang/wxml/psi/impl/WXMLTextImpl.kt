package com.zxy.ijplugin.wechat_miniprogram.lang.wxml.psi.impl

import com.intellij.psi.LiteralTextEscaper
import com.intellij.psi.impl.source.xml.XmlTextImpl

class WXMLTextImpl : XmlTextImpl() {
    override fun createLiteralTextEscaper(): LiteralTextEscaper<XmlTextImpl> {
        return WxmlRawTextEscaper(this)
    }
}
