package com.zxy.ijplugin.wechat_miniprogram.lang.wxml

import com.intellij.lang.injection.InjectedLanguageManager
import com.intellij.lang.annotation.HighlightSeverity
import com.intellij.openapi.vfs.newvfs.impl.VfsRootAccess
import com.intellij.psi.PsiErrorElement
import com.intellij.psi.util.PsiTreeUtil
import com.intellij.psi.xml.XmlText
import com.intellij.testFramework.fixtures.BasePlatformTestCase
import java.nio.file.Path

class WxmlInterpolationParsingTest : BasePlatformTestCase() {

    override fun setUp() {
        super.setUp()
        project.basePath?.let {
            VfsRootAccess.allowRootAccess(testRootDisposable, it)
        }
        VfsRootAccess.allowRootAccess(
                testRootDisposable,
                Path.of(System.getProperty("user.dir"), ".intellijPlatform").toString()
        )
    }

    fun testLogicalAndInterpolationInTextHasInjectedJs() {
        myFixture.configureByText(
                "index.wxml", """
            <web-view src="{{src}}">
                {{ a && b }}
            </web-view>
        """.trimIndent()
        )

        val xmlText = PsiTreeUtil.findChildOfType(myFixture.file, XmlText::class.java)
        assertNotNull(xmlText)

        val injectedFiles = InjectedLanguageManager.getInstance(project).getInjectedPsiFiles(xmlText!!)
        assertNotNull(injectedFiles)
        assertFalse(injectedFiles!!.isEmpty())
        assertEquals("( a && b )", injectedFiles.single().first.text)
        assertEmpty(PsiTreeUtil.collectElementsOfType(injectedFiles.single().first, PsiErrorElement::class.java))
    }

    fun testObjectSpreadInterpolationInTextHasNoParseErrors() {
        myFixture.configureByText(
                "index.wxml", """
            <web-view src="{{src}}">
                {{ ...ccc }}
            </web-view>
        """.trimIndent()
        )

        val xmlText = PsiTreeUtil.findChildOfType(myFixture.file, XmlText::class.java)
        assertNotNull(xmlText)

        val injectedFiles = InjectedLanguageManager.getInstance(project).getInjectedPsiFiles(xmlText!!)
        assertNotNull(injectedFiles)
        assertFalse(injectedFiles!!.isEmpty())
        assertEquals("({ ...ccc })", injectedFiles.single().first.text)

        val errors = PsiTreeUtil.collectElementsOfType(injectedFiles.single().first, PsiErrorElement::class.java)
        assertEmpty(errors)
    }

    fun testBitwiseAndInterpolationInTextHasNoErrorHighlighting() {
        myFixture.configureByText(
                "index.wxml", """
            <web-view src="{{src}}">
                {{ a & b }}
            </web-view>
        """.trimIndent()
        )

        val errorHighlights = myFixture.doHighlighting(HighlightSeverity.ERROR)
        assertEmpty(errorHighlights)
    }

    fun testLogicalAndInterpolationInTextHasNoErrorHighlighting() {
        myFixture.configureByText(
                "index.wxml", """
            <web-view src="{{src}}">
                {{ a && b }}
            </web-view>
        """.trimIndent()
        )

        val errorHighlights = myFixture.doHighlighting(HighlightSeverity.ERROR)
        assertEmpty(errorHighlights)
    }

    fun testObjectSpreadInterpolationInTextHasNoErrorHighlighting() {
        myFixture.configureByText(
                "index.wxml", """
            <web-view src="{{src}}">
                {{ ...ccc }}
            </web-view>
        """.trimIndent()
        )

        val errorHighlights = myFixture.doHighlighting(HighlightSeverity.ERROR)
        assertEmpty(errorHighlights)
    }
}
