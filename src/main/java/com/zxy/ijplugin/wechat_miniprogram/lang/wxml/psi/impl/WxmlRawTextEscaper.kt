package com.zxy.ijplugin.wechat_miniprogram.lang.wxml.psi.impl

import com.intellij.openapi.util.TextRange
import com.intellij.psi.LiteralTextEscaper
import com.intellij.psi.PsiLanguageInjectionHost

class WxmlRawTextEscaper<T : PsiLanguageInjectionHost>(host: T) : LiteralTextEscaper<T>(host) {

    override fun decode(rangeInsideHost: TextRange, outChars: StringBuilder): Boolean {
        outChars.append(rangeInsideHost.substring(myHost.text))
        return true
    }

    override fun getOffsetInHost(offsetInDecoded: Int, rangeInsideHost: TextRange): Int {
        val offset = rangeInsideHost.startOffset + offsetInDecoded
        return if (offset <= rangeInsideHost.endOffset) offset else -1
    }

    override fun isOneLine(): Boolean = false
}
