"""Populate Japanese PO files for docs-next.

Covers:
  D1 (hand-written pages):
    - index.md
    - guides/overview.md, history.md, terms.md, privacy.md
    - packages/index.md (category headings)
    - _handwritten/packages/visual_slam.md
  D2 (rosdoc2 common labels):
    - all packages/**/*.po have their shared exhale/breathe labels translated

Terms / Privacy use paragraph-aligned JP text from the legacy site
(triorb-amr-docs/docs/Terms.md, PrivacyPolicy.md) which has the same
heading / paragraph structure as the English source.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

import polib


REPO = Path(__file__).resolve().parents[2]
LOCALE = REPO / "docs-next" / "locale" / "ja" / "LC_MESSAGES"
LEGACY = REPO / "triorb-amr-docs" / "docs"


# ---------------------------------------------------------------------------
# Paragraph alignment: extract non-empty, non-blockquote-marker lines grouped
# into paragraphs, using the same splitter for JP and EN source files.
# ---------------------------------------------------------------------------
def split_paragraphs(md_text: str) -> List[str]:
    paras: List[str] = []
    buf: List[str] = []
    for line in md_text.splitlines():
        line = line.rstrip()
        if line.strip() == "":
            if buf:
                paras.append("\n".join(buf).strip())
                buf = []
        else:
            buf.append(line)
    if buf:
        paras.append("\n".join(buf).strip())
    return paras


def align_pairs(en_md: Path, jp_md: Path) -> Dict[str, str]:
    """Return {en_paragraph: jp_paragraph} keyed by paragraph order."""
    en_paras = split_paragraphs(en_md.read_text(encoding="utf-8"))
    jp_paras = split_paragraphs(jp_md.read_text(encoding="utf-8"))
    if len(en_paras) != len(jp_paras):
        print(
            f"  WARN paragraph count mismatch for {en_md.name}: "
            f"en={len(en_paras)}, jp={len(jp_paras)}"
        )
    mapping: Dict[str, str] = {}
    for en, jp in zip(en_paras, jp_paras):
        mapping[en] = jp
        # Also register heading-only forms. Sphinx lifts headings to their own
        # msgid without the leading '#' markers.
        m_en = re.match(r"^(#+)\s+(.*)$", en)
        m_jp = re.match(r"^(#+)\s+(.*)$", jp)
        if m_en and m_jp:
            mapping[m_en.group(2).strip()] = m_jp.group(2).strip()
    return mapping


def apply_mapping(po_path: Path, mapping: Dict[str, str]) -> int:
    """Set msgstr from mapping when our mapping has a translation for the msgid.

    Overwrites existing msgstr if present — important for entries that
    sphinx-intl marked `fuzzy` by inheriting stale text from a renamed msgid.
    Leaves msgstr alone if the msgid isn't in the mapping.
    """
    if not po_path.exists():
        print(f"  MISS {po_path.relative_to(REPO)}")
        return 0
    po = polib.pofile(str(po_path))
    hits = 0
    for entry in po:
        if entry.obsolete:
            continue
        if entry.msgid not in mapping:
            continue
        new_msgstr = mapping[entry.msgid]
        if entry.msgstr != new_msgstr or entry.fuzzy:
            entry.msgstr = new_msgstr
            # Clear fuzzy flag so Sphinx applies the translation.
            if "fuzzy" in entry.flags:
                entry.flags.remove("fuzzy")
            hits += 1
    po.save(str(po_path))
    return hits


# ---------------------------------------------------------------------------
# D1 manual dicts for the hand-written short pages.
# ---------------------------------------------------------------------------
INDEX_MD_DICT = {
    "TriOrb BASE Developer Guide": "TriOrb BASE 開発ガイド",
    "Developer documentation for TriOrb BASE. Covers API references for autonomous and collaborative navigation packages, operational guides, and the changelog.":
        "TriOrb BASE の開発者向けドキュメントです。自律移動・協調搬送パッケージの API リファレンス、運用ガイド、変更履歴をまとめています。",
    "User Guide": "ユーザーガイド",
    "Package API (rosdoc2)": "パッケージ API (rosdoc2)",
    "Legal": "法務",
    "Support": "サポート",
    "Source / Issues: [TriOrb-Inc/TriOrb-AMR-Documents](https://github.com/TriOrb-Inc/TriOrb-AMR-Documents)":
        "ソースコード / Issue: [TriOrb-Inc/TriOrb-AMR-Documents](https://github.com/TriOrb-Inc/TriOrb-AMR-Documents)",
    "Contact: `info@triorb.co.jp`": "お問い合わせ: `info@triorb.co.jp`",
    "Past versions": "過去バージョン",
    "Documentation for v1.2.4 and earlier is available in the legacy MkDocs archive.":
        "v1.2.4 以前のドキュメントは旧サイト (MkDocs) のアーカイブをご参照ください。",
    "[v1.2.4 (legacy site)](../v1.2.4/)": "[v1.2.4 (旧サイト)](../v1.2.4/)",
    "[v1.2.3 (legacy site)](../v1.2.3/)": "[v1.2.3 (旧サイト)](../v1.2.3/)",
    "[v1.2.2 (legacy site)](../v1.2.2/)": "[v1.2.2 (旧サイト)](../v1.2.2/)",
}

OVERVIEW_MD_DICT = {
    "Product Overview": "製品概要",
    "TriOrb BASE is an autonomous mobile robot (AMR) platform with omnidirectional motion realized by three omniwheels.":
        "TriOrb BASE は、3 つのオムニホイールによる全方位移動を実現する自律移動ロボット (AMR) プラットフォームです。",
    "This site provides:": "本サイトでは以下の情報を提供します:",
    "**Autonomous Navigation API**: ROS 2 topics / services / actions for driving the robot":
        "**自律移動 API**: ロボットを制御するための ROS 2 トピック / サービス / アクション",
    "**Collaborative Navigation API**: additional APIs for multi-robot cooperative transport":
        "**協調移動 API**: 複数台で連携搬送する場合の追加 API",
    "**Control ECU Library**: a Python library for sending commands to the TriOrb control ECU directly from a host PC":
        "**制御 ECU 通信ライブラリ**: 上位 PC から TriOrb 制御 ECU へ直接指令を送るための Python ライブラリ",
    "**Changelog / Terms of Service / Privacy Policy**": "**変更履歴 / 利用規約 / プライバシーポリシー**",
    "Before you start": "利用前に",
    "For hardware setup and initial software installation, refer to the separately distributed documents:":
        "ハードウェアのセットアップおよびソフトウェア導入手順は、別途配布される以下のドキュメントを参照してください:",
    "TriOrb BASE Operating Manual": "TriOrb BASE 取扱説明書",
    "Autonomous Navigation Package User Manual": "自律移動パッケージ ユーザーズマニュアル",
    "Upgrade Procedures": "アップグレード手順書",
    "This site focuses on the public API surface and change history of the ROS 2 / Python layer.":
        "本サイトは ROS 2 / Python レイヤの公開 API 仕様と変更履歴に特化しています。",
}

HISTORY_MD_DICT = {
    "Changelog": "変更履歴",
    "v1.2.5 (in progress)": "v1.2.5 (作業中)",
    "From this release the documentation stack moves to Sphinx + rosdoc2 + Furo. English is the source of truth; the Japanese site is produced from PO translations. Use the language switcher in the sidebar to swap between Japanese and English.":
        "本バージョンからドキュメント基盤を Sphinx + rosdoc2 + Furo に移行しました。英語を正となるソースとし、日本語版は PO 翻訳から生成しています。サイドバー上部の言語切替から日英を選択してください。",
    "Earlier changes are available in the legacy site linked above.":
        "それ以前の変更履歴は上記の旧サイトリンクから確認できます。",
}

PKG_INDEX_DICT = {
    "Package API": "パッケージ API",
    "Auto-generated API reference for ROS 2 packages under TriOrb-AMR-Package, produced by rosdoc2. Packages are grouped by subsystem; within each group they are sorted alphabetically.":
        "TriOrb-AMR-Package 配下の ROS 2 パッケージについて、rosdoc2 が自動生成した API リファレンスです。サブシステム別にグルーピングし、各グループ内では名前順に並べています。",
    "Drive & Navigation": "駆動・ナビゲーション",
    "SLAM": "SLAM",
    "Sensor I/O": "センサー I/O",
    "Safety Sensors": "セーフティセンサ",
    "OS / Infrastructure": "OS・基盤",
    "Fleet": "フリート",
    "Service": "サービス",
    "Interfaces": "インタフェース",
    "Other": "その他",
}

VISUAL_SLAM_DICT = {
    "Visual SLAM": "Visual SLAM",
    "Visual SLAM is TriOrb BASE's map building and self-localization engine based on stereo keyframe features. The implementation wraps the open-source [stella_vslam](https://github.com/stella-cv/stella_vslam) library — its internal API is considered implementation detail and is not covered in this reference.":
        "Visual SLAM は、ステレオキーフレーム特徴量にもとづく TriOrb BASE の地図生成・自己位置推定エンジンです。オープンソースの [stella_vslam](https://github.com/stella-cv/stella_vslam) を内部で利用していますが、ラッパーの内部 API は実装詳細として扱い、本リファレンスでは公開していません。",
    "Role on TriOrb BASE": "TriOrb BASE における役割",
    "Responsibility": "役割",
    "Description": "説明",
    "Map building": "地図生成",
    "Builds a 3D keyframe-based map while the robot is driven through the environment":
        "手動走行やリモコン走行中にステレオ特徴量から 3D キーフレーム地図を構築",
    "Self-localization": "自己位置推定",
    "Estimates 6-DoF robot pose at runtime by matching stereo features against the stored map":
        "保存済み地図とステレオ特徴量を照合して実行時に 6 自由度のロボット姿勢を推定",
    "Map export": "地図エクスポート",
    "Exports the 3D map to a 2D occupancy representation used by downstream navigation":
        "ナビゲーションが利用する 2D 占有格子表現に 3D 地図を変換",
    "Map I/O": "地図 I/O",
    "Saves / loads map files to the robot controller and PC":
        "ロボットコントローラや PC との間で地図ファイルの保存・読み込みを実施",
    "Interfaces you care about": "関連する API",
    "Day-to-day interaction is through higher-level APIs, not through Visual SLAM directly:":
        "運用では Visual SLAM を直接操作せず、以下の上位 API 経由で利用します:",
    "`triorb_vslam_tf` — publishes VSLAM-derived pose as TF":
        "`triorb_vslam_tf` — VSLAM 由来の姿勢を TF として配信",
    "`trirob_vslam_tf_bridge` — bridges VSLAM to navigation pose":
        "`trirob_vslam_tf_bridge` — VSLAM 姿勢をナビゲーション用姿勢へブリッジ",
    "`triorb_dead_reckoning` — fuses VSLAM, odometry, and IMU for robust pose":
        "`triorb_dead_reckoning` — VSLAM・オドメトリ・IMU を統合し堅牢な自己位置を推定",
    "The WebAPI's map save / load / switch operations":
        "WebAPI の地図保存・読み込み・切替操作",
    "See those packages for the public topic / service surface.":
        "公開されているトピック / サービスは各パッケージのページを参照してください。",
    "Related": "関連",
    "[triorb_vslam_tf](triorb_vslam_tf/index.md)": "[triorb_vslam_tf](triorb_vslam_tf/index.md)",
    "[trirob_vslam_tf_bridge](trirob_vslam_tf_bridge/index.md)": "[trirob_vslam_tf_bridge](trirob_vslam_tf_bridge/index.md)",
    "[triorb_dead_reckoning](triorb_dead_reckoning/index.md)": "[triorb_dead_reckoning](triorb_dead_reckoning/index.md)",
}


# ---------------------------------------------------------------------------
# D2 rosdoc2 / exhale / breathe labels repeated across every package.
# Single dict applied to every packages/**/*.po.
# ---------------------------------------------------------------------------
ROSDOC2_LABEL_DICT = {
    "Class Documentation": "クラスドキュメント",
    "Message Definitions": "メッセージ定義",
    "Standard Documents": "標準ドキュメント",
    "Nested Relationships": "ネスト関係",
    "Nested Types": "ネスト型",
    "Inheritance Relationships": "継承関係",
    "Derived Type": "派生型",
    "Derived Types": "派生型",
    "Base Type": "基底型",
    "Base Types": "基底型",
    "Public Functions": "Public メンバ関数",
    "Public Static Functions": "Public 静的メンバ関数",
    "Public Members": "Public メンバ",
    "Public Static Members": "Public 静的メンバ",
    "Public Types": "Public 型",
    "Public Types Documentation": "Public 型ドキュメント",
    "Protected Functions": "Protected メンバ関数",
    "Protected Static Functions": "Protected 静的メンバ関数",
    "Protected Members": "Protected メンバ",
    "Protected Types": "Protected 型",
    "Private Functions": "Private メンバ関数",
    "Private Members": "Private メンバ",
    "Functions": "関数",
    "Variables": "変数",
    "Enums": "列挙型",
    "Typedefs": "型定義",
    "Defines": "マクロ定義",
    "Classes": "クラス",
    "Structs": "構造体",
    "Namespaces": "名前空間",
    "Namespace": "名前空間",
    "Directories": "ディレクトリ",
    "Directory": "ディレクトリ",
    "Files": "ファイル",
    "File": "ファイル",
    "Class Hierarchy": "クラス階層",
    "Namespace Hierarchy": "名前空間階層",
    "File Hierarchy": "ファイル階層",
    "Page Hierarchy": "ページ階層",
    "Full API": "全 API",
    "Defined in": "定義場所",
    "Source": "ソース",
    "Contents": "目次",
    "Overview": "概要",
    "Macros": "マクロ",
    "C++ API": "C++ API",
    "Definition": "定義",
    "Definition (sick_plc_wrapper.hpp)": "定義 (sick_plc_wrapper.hpp)",
    "Includes": "インクルード",
    "Included By": "被インクルード",
    "Program Listing": "プログラムリスト",
    "This is a ROS message definition.": "ROS メッセージ定義です。",
    "Changelog": "変更履歴",
    "License": "ライセンス",
    "Package": "パッケージ",
    "PACKAGE": "パッケージ",
    "README": "README",
    "Page Contents": "ページ内容",
    "Sub-namespaces": "サブ名前空間",
    "Unions": "共用体",
    "Template Parameter Order": "テンプレート引数の順序",
    "Template Parameters": "テンプレート引数",
    "Parameters": "引数",
    "Returns": "戻り値",
    "Return": "戻り値",
    "Return Value": "戻り値",
    "Throws": "例外",
    "See also": "関連項目",
    "Warning": "警告",
    "Note": "注記",
    "Attention": "注意",
    "Deprecated": "非推奨",
    "Author": "作者",
    "Copyright": "著作権",
    "Index": "索引",
    "Module Index": "モジュール索引",
    "Search Page": "検索ページ",
}


def populate_d1() -> None:
    simple_dicts = {
        "index.po": INDEX_MD_DICT,
        "guides/overview.po": OVERVIEW_MD_DICT,
        "guides/history.po": HISTORY_MD_DICT,
        "packages/index.po": PKG_INDEX_DICT,
        "_handwritten/packages/visual_slam.po": VISUAL_SLAM_DICT,
    }
    for rel, mapping in simple_dicts.items():
        n = apply_mapping(LOCALE / rel, mapping)
        print(f"D1 {rel}: {n} translations")

    print("D1 Terms: paragraph align from legacy JP")
    terms_map = align_pairs(LEGACY / "Terms.en.md", LEGACY / "Terms.md")
    n = apply_mapping(LOCALE / "guides" / "terms.po", terms_map)
    print(f"D1 guides/terms.po: {n} translations")

    print("D1 Privacy: paragraph align from legacy JP")
    priv_map = align_pairs(LEGACY / "PrivacyPolicy.en.md", LEGACY / "PrivacyPolicy.md")
    n = apply_mapping(LOCALE / "guides" / "privacy.po", priv_map)
    print(f"D1 guides/privacy.po: {n} translations")


def populate_d2() -> None:
    pkg_root = LOCALE / "packages"
    if not pkg_root.is_dir():
        print("D2 skipped: no packages/ locale tree yet")
        return
    total_files = 0
    total_hits = 0
    for po_path in pkg_root.rglob("*.po"):
        n = apply_mapping(po_path, ROSDOC2_LABEL_DICT)
        if n:
            total_files += 1
            total_hits += n
    print(f"D2 rosdoc2 labels applied to {total_files} files: {total_hits} msgstr set")


if __name__ == "__main__":
    populate_d1()
    populate_d2()
