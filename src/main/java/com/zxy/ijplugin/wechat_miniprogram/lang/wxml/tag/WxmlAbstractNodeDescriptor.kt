/*
 *    Copyright (c) [2019] [zxy]
 *    [wechat-miniprogram-plugin] is licensed under the Mulan PSL v1.
 *    You can use this software according to the terms and conditions of the Mulan PSL v1.
 *    You may obtain a copy of Mulan PSL v1 at:
 *       http://license.coscl.org.cn/MulanPSL
 *    THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
 *    IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
 *    PURPOSE.
 *    See the Mulan PSL v1 for more details.
 */

package com.zxy.ijplugin.wechat_miniprogram.lang.wxml.tag

import com.intellij.json.psi.JsonProperty
import com.intellij.psi.PsiElement
import com.intellij.psi.xml.XmlTag
import com.intellij.xml.XmlAttributeDescriptor
import com.intellij.xml.XmlElementDescriptor
import com.intellij.xml.impl.schema.AnyXmlAttributeDescriptor

class WxmlAbstractNodeDescriptor(
        private val element: JsonProperty
) : WXMLBasicElementDescriptor() {
    override fun getDefaultValue(): String? {
        return null
    }

    override fun getName(context: PsiElement?): String {
        return this.name
    }

    override fun getName(): String {
        return this.element.name
    }

    override fun getElementsDescriptors(context: XmlTag?): Array<XmlElementDescriptor> {
        return emptyArray()
    }

    override fun init(element: PsiElement?) {
    }

    override fun getDefaultName(): String {
        return this.name
    }

    override fun getQualifiedName(): String {
        return this.name
    }

    override fun getDeclaration(): PsiElement {
        return this.element
    }

    override fun getAttributeDescriptor(attributeName: String, context: XmlTag?): XmlAttributeDescriptor? {
        return super.getAttributeDescriptor(attributeName, context) ?: AnyXmlAttributeDescriptor(attributeName)
    }
}
