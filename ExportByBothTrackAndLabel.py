import pyaudacity as pa
import json
import sys
import os
"""
argumenty programu wczytywane z linii polecen:
1 - sciezka do pliku outputowego, w rzeczywistosci bedzie w tej lokacji wiele plikow
2 - sciezka do Etykiet(Labels) zapisanych w formacie .txt
3 - liczba trackow, wliczajac track z Etykietami(Labels)


UWAGA: program zaklada, ze pole 'SOLO' NIE JEST zaznaczone na zadnym tracku. jesli ktorykolwiek ma zaznaczone solo podczas dzialania programu to program nie zadziala poprawnie

Ponadto zaklada on ze track z Labelami jest na samej gorze. Track z labelami tez liczy sie jako track na potrzeby argv[3]
argv[3] okresla liczbe trackow w projekcie audacity. W te liczbe wlicza sie track w ktorym sa labele

Do tego program zaklada ze w audacity w zakladce 'Edit -> Preferences -> Modules' pole mod-script-pipe jest zaznaczone na 'Enabled'. Jesli nie jest to trzeba ustawic je na enabled
a potem wylaczyc Audacity i wlaczyc jeszcze raz.

Przed wlaczeniem programu nalezy sie upewnic, ze w zakladce 'File -> Export Audio' wybrano juz folder docelowy i format, w ktorym maja sie znalezc wyeksportowane pliki.
'Audio options' ma byc ustawione na stereo, a 'Export range' na Multiple Files.
Nalezy tez ustawic 'Split files based on:' na 'Labels', a 'Name files' ustawic na 'Using Label/TrackName'.
Oprocz tego nalezy sie upewnic, ze checkbox 'Overwrite existing files' jest zaznaczony.
Po wykonaniu wszystkich tych czynnosci TRZEBA zamknac okno 'Export Audio', zeby program zadzialal prawidlowo.

Uruchomienie programu wymaga wlaczonego w Audacity projektu.
Jesli jest wlaczonych kilka projektow na raz, to program odpali sie dla okna, ktore ostatnie zostalo wlaczone.

Z tego miejsca chcialbym powiedziec, ze pierdole API Audacity do scriptingu.
A, i w ogole program nie dziala jak dzwiek na jednej sciezce jest dluzszy niz 2h46min,
ale to akurat specjalnie. Ponownie API do Audacity jest chujowe. Pierdole.

Przykladowe wywolanie programu:
python ExportByBothTrackAndLabel.py "D:\SoundAssets\Music\ExportedAudio\DebugPiaMaterSeparated\OutputAudio.wav" "D:\SoundAssets\Music\ExportedAudio\DebugPiaMaterSeparated\labels\Labels1.txt" 17

niestety lepiej przekazywac pelna sciezke do plikow
"""

def wczytaj_dane_z_pliku(file_path):
    data_list = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            start_time = float(parts[0])
            end_time = float(parts[1])
            label = parts[2]
            data_list.append([start_time, end_time, label])
    return data_list



def export_labels():
    #pa.do('FirstTrack')
    
    #pa.do("TrackMute")
    #pa.do('GetInfo: Type="Tracks"')

    
    try:
        print(f"Argument numer 3: {sys.argv[3]}")
        print(f"Typ argumentu numer 3: {type(sys.argv[1])}")
        track_count = int(sys.argv[3])
        print(f"Typ argumentu 3 po konwersji: {type(track_count)}")
    except:
        print("ERROR:\nProgram wymaga podania ilosci trackow jako trzeci argument.\nUWAGA: track z labelami tez sie w to wlicza\nprogram zostaje zamkniety'")
        exit(0)

    try:
        print(f"Argument numer 2: {sys.argv[2]}")
        print(f"Typ argumentu numer 1: {type(sys.argv[2])}")
        label_file_path = sys.argv[2]
        print(f"Typ argumentu 2 po konwersji: {type(label_file_path)}")
    except:
        print("ERROR:\nProgram wymaga podania sciezki do pliku z danymi etykiet jako drugi argument.\nprogram zostaje zamkniety'")
        exit(0)

    try:
        print(f"Argument numer 1: {sys.argv[1]}")
        print(f"Typ argumentu numer 1: {type(sys.argv[1])}")
        output_file_path = sys.argv[1]
        print(f"Typ argumentu 1 po konwersji: {type(output_file_path)}")
    except:
        print("ERROR:\nProgram wymaga podania sciezki do pliku wyjsciowego jako pierwszy argument.\nUWAGA: track z labelami tez sie w to wlicza\nprogram zostaje zamkniety'")
        exit(0)
    
        
    #JD pierdole to
    #first track czyli ten z labelami
    #pa.do('FirstTrack')

    #testowo
    #pa.do('NextTrack')

    #chociaz dzieki temu wiemy ze pierdolone export2 dziala tylko jest chujowe
    #pa.do('SelectAll')
    #pa.do('SelAllTracks')

    #wczytanie danych z etykiet

    #ten segment dziala chociaz - tracki sa numerowane od 0 w audacity API jakby co
    
    #pa.do('SelectTracks: Track=1')
    #pa.do('SelectTime: Start=0 End=9999')
    #pa.do('Export2: Filename="D:\SoundAssets\Music\ExportedAudio\DebugPiaMaterSeparated\ExportedTest.wav" NumChannels=2')
    

    pa.do('SelectTracks: Track=1')
    #program wlasciwy: selectowanie kazdego tracka po kolei-> selectowanie time'u kazdego labela wewn. danego tracka->exportowanie wycinka wzgledem tracku i labela do pliku -> zmiana nazwy tego pliku
    #zalozenie jest takie ze jest 5 labeli: Intro, LoopA, Transition, LoopB, Outro
    label_data_list = wczytaj_dane_z_pliku(label_file_path)
    print("Struktura danych etykiet:")
    print(label_data_list)
    print("len(label_data_list[0]) =", len(label_data_list[0]))
    for i in range(track_count-1):
        pa.do(f'SelectTracks: Track={i+1}') #+1 bo tracku z labelami nie chcemy eksportowac, i tak audio na nim jest puste
        for j in range(len(label_data_list)):
            pa.do(f'SelectTime: Start={label_data_list[j][0]} End={label_data_list[j][1]}')
            pa.do(f'Export2: Filename={output_file_path} NumChannels=2')
            #teraz trzeba zmienic nazwe pliku
            #os.rename(oldname,newname)
            #-4 bo zakladam ze pliki sa .wav
            new_path = output_file_path[:-4]
            #print(new_path)
            os.rename(output_file_path, f'{new_path}{label_data_list[j][2]}Track{i+1}.wav')

    #pa.do('SelectTracks: Track=5')
    #pa.do('ShiftDown')
    #pa.do('TrackSolo')
    #pa.export_sel()
    #pa.do('Export2: Filename="DebugPiaMater.wav" NumChannels=2')
    #pa.do('ExportSel')
    #pa.do('ExportAudio')
    #pa.do('ExportLabels')
    #pa.do('ExportMultiple: Format="WAV" ExportPath="D:\SoundAssets\Music\ExportedAudio" FileNaming="Label"')
    



if __name__ == "__main__":
    export_labels()
