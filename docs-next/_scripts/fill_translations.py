"""Populate Japanese PO files for docs-next (D1 hand-written pages).

Covers:
  - index.md
  - guides/overview.md, history.md, terms.md, privacy.md
  - packages/index.md (category headings)
  - packages/visual_slam.md
  (7 hand-written docs total)

Terms / Privacy use paragraph-aligned JP text from the legacy site
(triorb-amr-docs/docs/Terms.md, PrivacyPolicy.md) which has the same
heading / paragraph structure as the English source.

D2 (rosdoc2 common labels) was retired in the Phase 4 B plan: rosdoc2
API pages ship in English only to avoid the full-rebuild cascade that
every .mo change triggers. A retired reference dict remains below for
future reactivation.
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
    # Save only when something actually changed — avoid bumping mtime on
    # untouched PO files, which would force sphinx-intl to rebuild every .mo
    # and cascade into Sphinx invalidating all docs.
    if hits:
        po.save(str(po_path))
    return hits


# ---------------------------------------------------------------------------
# D1 manual dicts for the hand-written short pages.
# ---------------------------------------------------------------------------
INDEX_MD_DICT = {
    "TriOrb BASE Developer Guide": "TriOrb BASE 開発ガイド",
    "Developer documentation for TriOrb BASE. Covers the ROS 2 API reference for the autonomous navigation package, the host-side control ECU library, operational guides, and the changelog.":
        "TriOrb BASE の開発者向けドキュメントです。自律移動パッケージの ROS 2 API リファレンス、上位側制御 ECU 通信ライブラリ、運用ガイド、変更履歴をまとめています。",
    "User Guide": "ユーザーガイド",
    "Package API (rosdoc2)": "パッケージ API (rosdoc2)",
    "REST API": "REST API",
    "REST API (external site)": "REST API（別サイト）",
    "MCP": "MCP",
    "MCP server (external)": "MCP サーバー（別サイト）",
    "How to connect from ChatGPT or Claude": "ChatGPT や Claude などから接続する方法",
    "Legal": "法務",
    "Support": "サポート",
    "Source / Issues: [TriOrb-Inc/TriOrb-AMR-Documents](https://github.com/TriOrb-Inc/TriOrb-AMR-Documents)":
        "ソースコード / Issue: [TriOrb-Inc/TriOrb-AMR-Documents](https://github.com/TriOrb-Inc/TriOrb-AMR-Documents)",
    "Contact: `info@triorb.co.jp`": "お問い合わせ: `info@triorb.co.jp`",
    "[REST API](https://triorb-inc.github.io/TriOrb-AMR-Robot-Controller/) (separate site)":
        "[REST API](https://triorb-inc.github.io/TriOrb-AMR-Robot-Controller/)（別サイト）",
    "[How to connect from ChatGPT or Claude](https://mcp.triorb-cloud.com/docs/setup-guide)":
        "[ChatGPT や Claude などから接続する方法](https://mcp.triorb-cloud.com/docs/setup-guide)",
    "[MCP server](https://mcp.triorb-cloud.com/mcp/) — public TriOrb Model Context Protocol endpoint, usable from any MCP-capable AI client.":
        "[MCP サーバー](https://mcp.triorb-cloud.com/mcp/) — TriOrb 提供の Model Context Protocol エンドポイント。MCP 対応の AI クライアントから誰でもご利用いただけます。",
    "Past versions": "過去バージョン",
    "Documentation for v1.2.3 and earlier is available in the legacy MkDocs archive.":
        "v1.2.3 以前のドキュメントは旧サイト (MkDocs) のアーカイブをご参照ください。",
    "[v1.2.3 (legacy site)](../../v1.2.3/)": "[v1.2.3 (旧サイト)](../../v1.2.3/)",
    "[v1.2.2 (legacy site)](../../v1.2.2/)": "[v1.2.2 (旧サイト)](../../v1.2.2/)",
    "See the [top-level version picker](../../) for a cross-version landing page.":
        "版の横断トップは [バージョンピッカー](../../) をご利用ください。",
}

OVERVIEW_MD_DICT = {
    "Product Overview": "製品概要",
    "TriOrb BASE is an autonomous mobile robot (AMR) platform built around a novel **ball-drive omnidirectional motion mechanism** that addresses the \"external disturbance handling, positioning accuracy, and load capacity\" trade-offs that classical omnidirectional platforms have struggled with.":
        "TriOrb BASE は、独自の**球体駆動式全方向移動機構**を搭載した自律移動ロボット (AMR) プラットフォームです。従来の全方向移動プラットフォームでは両立が難しかった「外乱走破性・位置決め精度・耐荷重」を同時に成立させる独自構造です。",
    "Representative specs: standard φ100 sphere, load up to ~300 kg. Refer to the TriOrb website for the latest hardware figures.":
        "代表仕様: 標準球径 φ100、可搬能力 約 300 kg。最新のハードウェア諸元は TriOrb コーポレートサイト等をご参照ください。",
    "This site provides:": "本サイトでは以下の情報を提供します:",
    "**Autonomous Navigation API**: ROS 2 topics / services / actions for driving the robot":
        "**自律移動 API**: ロボットを制御するための ROS 2 トピック / サービス / アクション",
    "**Control ECU Library**: a Python library for sending commands to the TriOrb control ECU directly from a host PC":
        "**制御 ECU 通信ライブラリ**: 上位 PC から TriOrb 制御 ECU へ直接指令を送るための Python ライブラリ",
    "**REST API**: browser-facing HTTP API for the robot controller ([separate site](https://triorb-inc.github.io/TriOrb-AMR-Robot-Controller/))":
        "**REST API**: ロボットコントローラ向けの HTTP API（[別サイト](https://triorb-inc.github.io/TriOrb-AMR-Robot-Controller/)）",
    "**Changelog / Terms of Service / Privacy Policy**": "**変更履歴 / 利用規約 / プライバシーポリシー**",
    "Before you start": "利用前に",
    "For hardware setup and initial software installation, refer to the TriOrb User Documents portal, which aggregates the **TriOrb BASE Operating Manual**, **Autonomous Navigation Package User Manual**, and **Upgrade Procedures**:":
        "ハードウェアのセットアップおよびソフトウェア導入手順は、**TriOrb BASE 取扱説明書**・**自律移動パッケージ ユーザーズマニュアル**・**アップグレード手順書**をまとめた TriOrb User Documents ポータルを参照してください:",
    "[TriOrb User Documents (Notion)](https://triorb.notion.site/2afb60b1eaf380dd8e6acade491a29d6?v=2afb60b1eaf381f4a558000ca9c9461d)":
        "[TriOrb User Documents (Notion)](https://triorb.notion.site/2afb60b1eaf380dd8e6acade491a29d6?v=2afb60b1eaf381f4a558000ca9c9461d)",
    "Detailed hardware manuals for non-standard models are distributed separately on a per-project basis.":
        "標準機以外のハードウェア詳細マニュアルは個別配布となります。",
    "This site focuses on the public API surface and change history of the ROS 2 / Python layer. The [REST API](https://triorb-inc.github.io/TriOrb-AMR-Robot-Controller/) is also available when a browser-only integration is preferred.":
        "本サイトは ROS 2 / Python レイヤの公開 API 仕様と変更履歴に特化しています。ブラウザのみで連携したい場合は [REST API](https://triorb-inc.github.io/TriOrb-AMR-Robot-Controller/) もご利用いただけます。",
}

HISTORY_MD_DICT = {
    "Changelog": "変更履歴",
    "v1.2.4": "v1.2.4",
    "Per-release details are published on GitHub. This page summarizes the highlights of the latest release in plain prose; refer to the GitHub release notes for exact PR / commit lists. Earlier releases remain on the legacy MkDocs archive ([v1.2.3](../../v1.2.3/TriOrb-AMR-Package/History/), [v1.2.2](../../v1.2.2/TriOrb-AMR-Package/History/)).":
        "リリースごとの詳細は GitHub Release ページで公開しています。本ページでは最新リリースの主な変更内容を要約のみ掲載します（PR / コミットの正確な一覧はリリースノートをご参照ください）。それ以前のリリースは旧サイト（[v1.2.3](../../v1.2.3/TriOrb-AMR-Package/History/), [v1.2.2](../../v1.2.2/TriOrb-AMR-Package/History/)）に残しています。",
    "Documentation stack switches to Sphinx + rosdoc2 + Furo. English is the source of truth; the Japanese site is produced from PO translations. Use the language switcher in the sidebar to swap between Japanese and English.":
        "本バージョンからドキュメント基盤を Sphinx + rosdoc2 + Furo に移行しました。英語を正となるソースとし、日本語版は PO 翻訳から生成しています。サイドバー上部の言語切替から日英を選択してください。",
    "Headline functional changes in the `1.2.4.2` release (2026-04-07):":
        "`1.2.4.2` リリース（2026-04-07）の主な機能変更:",
    "**Navigation / drive control**: tidied up `stop` / `pause` delay and wait-time coordination with `snr_mux`, and reworked how the PICO connection timeout is handled. Goal XY judgment is now elliptical and idle-state navigation loop input reset is fixed.":
        "**ナビゲーション / 走行制御**: `stop` / `pause` の遅延や待機時間の `snr_mux` 連携を整理し、PICO 接続タイムアウトの扱いを見直しました。ゴール XY 判定を楕円化し、idle 中の navigation loop 入力リセット不具合を修正しました。",
    "**Manual operation / gamepad**: axis zero-range handling; suppress publish during autonomous motion; manual block stop / safe run controls; improved deadzone behavior.":
        "**手動操作 / gamepad**: 軸の zero range 対応、自律走行中の publish 抑止、manual block stop / safe run 制御、deadzone 処理を改善。",
    "**VSLAM / mapping / camera / MQTT**: restart VSLAM against the last loaded map; tracked-landmarks overlay; log preservation on abnormal termination. `run_mapping.sh` shows startup progress; camera now handles `AutoGainTarget`, scalar parameter parsing, and camera-disconnect scenarios; MQTT has improved reconnection resilience and startup-time client configuration injection.":
        "**VSLAM / マッピング / カメラ / MQTT**: 最後に読み込んだ map での VSLAM 再起動、tracked landmarks 表示、異常終了時のログ保存に対応。`run_mapping.sh` の起動進捗表示、camera の `AutoGainTarget` / 単一値パラメータ解析 / 未接続時挙動、MQTT の接続復旧性と起動時 client 設定注入を改善。",
    "**GUI / platform / diagnostics**: updated `gui/html` and `gui/launcher`; fixed topic names when `ROS_PREFIX` is applied; beacon DDS priority adjustment. Offline local installer bundle; `dead_reckoning` ISAM removal; IMU bypass/verification logging.":
        "**GUI / プラットフォーム / 診断**: `gui/html` / `gui/launcher` を更新、`ROS_PREFIX` 適用時の topic 名を修正、beacon DDS 優先度を調整。オフライン用ローカルインストーラバンドル、`dead_reckoning` の ISAM 廃止、IMU 確認用バイパスログ機能を追加。",
    "Full release notes:\n[TriOrb-AMR-Package 1.2.4.2](https://github.com/TriOrb-Inc/TriOrb-AMR-Package/releases/tag/1.2.4.2)":
        "リリースノート全文:\n[TriOrb-AMR-Package 1.2.4.2](https://github.com/TriOrb-Inc/TriOrb-AMR-Package/releases/tag/1.2.4.2)",
    "Notable merged PRs: #405 (`dev/std1.2.4` rollup), #397 (PICO timeout and `snr_mux` wait-time parameterization), #388 (`triorb_gamepad` axis zero range), #378 (release/std1.2.4 navigation stabilization and Bison feature landing).":
        "主な取り込み PR: #405（`dev/std1.2.4` 反映）、#397（PICO timeout と `snr_mux` 待機時間パラメータ化）、#388（`triorb_gamepad` の axis zero range 対応）、#378（release/std1.2.4 向けナビ / 協調制御安定化と Bison 周辺機能反映）。",
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
    "Interfaces": "インタフェース",
    "TriOrb が公開している ROS 2 メッセージ / サービス / アクション定義の一覧です。 各 Interface パッケージは `submodules/TriOrb-AMR-Package/pkgs/TriOrb-ROS2-Types/` 配下で 配布されており、他のノード実装がインポートして利用します.":
        "TriOrb が公開している ROS 2 メッセージ / サービス / アクション定義の一覧です。各 Interface パッケージは `submodules/TriOrb-AMR-Package/pkgs/TriOrb-ROS2-Types/` 配下で配布されており、他のノード実装がインポートして利用します。",
}

VISUAL_SLAM_DICT = {
    "Visual SLAM": "Visual SLAM",
    "Visual SLAM is TriOrb BASE's map building and self-localization engine based on stereo keyframe features. Its internal wrapper API is considered implementation detail and is not covered in this reference.":
        "Visual SLAM は、ステレオキーフレーム特徴量にもとづく TriOrb BASE の地図生成・自己位置推定エンジンです。内部ラッパーの API は実装詳細として扱い、本リファレンスでは公開していません。",
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
    "API": "API",
    "Visual SLAM itself does not expose a public ROS 2 API. Day-to-day interaction is through higher-level packages that consume its output:":
        "Visual SLAM 自体は公開 ROS 2 API を提供しません。運用では出力を利用する以下の上位パッケージを経由します:",
    "Package": "パッケージ",
    "Role": "役割",
    "[`triorb_vslam_tf`](triorb_vslam_tf/index.md)": "[`triorb_vslam_tf`](triorb_vslam_tf/index.md)",
    "Publishes VSLAM-derived pose as TF.": "VSLAM 由来の姿勢を TF として配信。",
    "[`trirob_vslam_tf_bridge`](trirob_vslam_tf_bridge/index.md)": "[`trirob_vslam_tf_bridge`](trirob_vslam_tf_bridge/index.md)",
    "Bridges VSLAM to navigation pose.": "VSLAM 姿勢をナビゲーション用姿勢へブリッジ。",
    "[`triorb_dead_reckoning`](triorb_dead_reckoning/index.md)": "[`triorb_dead_reckoning`](triorb_dead_reckoning/index.md)",
    "Fuses VSLAM, odometry, and IMU for robust pose.": "VSLAM・オドメトリ・IMU を統合し堅牢な自己位置を推定。",
    "[REST API](https://triorb-inc.github.io/TriOrb-AMR-Robot-Controller/)": "[REST API](https://triorb-inc.github.io/TriOrb-AMR-Robot-Controller/)",
    "Map save / load / switch operations over HTTP.": "地図保存・読み込み・切替操作（HTTP）。",
    "See each package's API page for its public topics, services, and actions.":
        "公開されているトピック / サービス / アクションは各パッケージの API ページを参照してください。",
}


# ---------------------------------------------------------------------------
# NOTE: D2 (rosdoc2 common labels) has been retired. Per the "B plan" pivot
# in Phase 4, rosdoc2-generated API pages ship in English only. The
# packages/** PO tree was removed from the repo; this dict is kept for
# historical reference only and is no longer applied.
# ---------------------------------------------------------------------------
_RETIRED_ROSDOC2_LABEL_DICT = {
    "Class Documentation": "クラスドキュメント",
    "Struct Documentation": "構造体ドキュメント",
    "Enum Documentation": "列挙型ドキュメント",
    "Function Documentation": "関数ドキュメント",
    "Define Documentation": "マクロ定義ドキュメント",
    "Typedef Documentation": "型定義ドキュメント",
    "Variable Documentation": "変数ドキュメント",
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
    "**Source**": "**ソース**",
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
        # Sphinx reads translations for `packages/visual_slam.md` (which is
        # copied from `_handwritten/packages/`) at `packages/visual_slam.po`.
        # The `_handwritten/` tree is excluded from the build, so writing to
        # `_handwritten/packages/visual_slam.po` had no effect.
        "packages/visual_slam.po": VISUAL_SLAM_DICT,
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


if __name__ == "__main__":
    populate_d1()
