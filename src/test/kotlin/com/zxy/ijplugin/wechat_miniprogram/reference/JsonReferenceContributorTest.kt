package com.zxy.ijplugin.wechat_miniprogram.reference

import com.intellij.openapi.vfs.newvfs.impl.VfsRootAccess
import com.intellij.psi.PsiFileSystemItem
import com.intellij.testFramework.fixtures.BasePlatformTestCase
import java.nio.file.Path

class JsonReferenceContributorTest : BasePlatformTestCase() {

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

    fun testEntryPagePathResolvesToPageFile() {
        myFixture.addFileToProject("pages/index/index.js", "Page({})")
        myFixture.configureByText(
                "app.json", """
            {
              "pages": [],
              "entryPagePath": "pages/index/ind<caret>ex"
            }
        """.trimIndent()
        )

        assertReferenceResolvesTo("index.js")
    }

    fun testSubPackagePagesResolveFromSubPackageRoot() {
        myFixture.addFileToProject("packageA/pages/index/index.js", "Page({})")
        myFixture.configureByText(
                "app.json", """
            {
              "pages": [],
              "subPackages": [
                {
                  "root": "packageA",
                  "pages": [
                    "pages/index/ind<caret>ex"
                  ]
                }
              ]
            }
        """.trimIndent()
        )

        assertReferenceResolvesTo("index.js")
    }

    fun testTabBarPagePathResolvesToPageFile() {
        myFixture.addFileToProject("pages/library/index.js", "Page({})")
        myFixture.configureByText(
                "app.json", """
            {
              "pages": [],
              "tabBar": {
                "list": [
                  {
                    "pagePath": "pages/library/ind<caret>ex",
                    "text": "Library"
                  }
                ]
              }
            }
        """.trimIndent()
        )

        assertReferenceResolvesTo("index.js")
    }

    private fun assertReferenceResolvesTo(fileName: String) {
        val reference = myFixture.file.findReferenceAt(myFixture.caretOffset)
        assertNotNull(reference)
        val target = reference?.resolve() as? PsiFileSystemItem
        assertNotNull(target)
        assertEquals(fileName, target?.name)
    }
}
