unit Steuerung;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, Forms, Controls, Graphics, Dialogs, ExtCtrls, StdCtrls;

type

  { TForm1 }

  TForm1 = class(TForm)
    Button1: TButton;
    Button2: TButton;
    Button3: TButton;
    Button4: TButton;
    Steuerelement: TShape;
    Zone: TBevel;
    Shape1: TShape;
    procedure Button1Click(Sender: TObject);
    procedure Button2Click(Sender: TObject);
    procedure Button3Click(Sender: TObject);
    procedure Button4Click(Sender: TObject);
  private

  public

  end;

var
  Form1: TForm1;

implementation

{$R *.lfm}

{ TForm1 }

procedure TForm1.Button1Click(Sender: TObject);
begin
     Shape1.Top := Shape1.Top - 15;
end;

procedure TForm1.Button2Click(Sender: TObject);
begin
     Shape1.Left := Shape1.Left - 15;
end;

procedure TForm1.Button3Click(Sender: TObject);
begin
     Shape1.Left := Shape1.Left + 15;
end;

procedure TForm1.Button4Click(Sender: TObject);
begin
     Shape1.Top := Shape1.Top + 15;
end;

end.


