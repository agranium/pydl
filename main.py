"""
pyDL

Python と Selenium を使用したCLIダウンローダー。
Chromeのプロファイルを指定するとキャッシュを流用できる。
"""


import click
import json
import dl


@click.group()
@click.option('--incomplete', '-i', type=str, default='./incomplete', help='Incomplete Files Directory.')
@click.option('--download', '-d', type=str, default='./download', help='Downloaded Files Directory.')
@click.option('--profile', '-p', type=str, default='./profile', help='Profile Directory.')
@click.option('--headless', '-h', type=bool, is_flag=True, help='Running with Headless Browzer.')
@click.pass_context
def cmd(ctx, incomplete, download, profile, headless):
    ctx.obj["incomplete"] = incomplete
    ctx.obj["download"] = download
    ctx.obj["profile"] = profile
    ctx.obj["headless"] = headless


@cmd.command()
@click.argument('queue_file', nargs=1)
@click.pass_context
def down(ctx, queue_file):
    down = dl.Downloader(
        ctx.obj["incomplete"],
        ctx.obj["download"],
        ctx.obj["profile"],
        ctx.obj["headless"]
        )
    down.run(queue_file)


@cmd.command()
@click.argument('queue_file', nargs=1)
@click.pass_context
def init(ctx, queue_file):
    with open(queue_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "queue": [],
                "downloading": [],
                "finished": []
            },
            f, indent=2, ensure_ascii=False
        )


if __name__ == "__main__":
    cmd(obj={})
