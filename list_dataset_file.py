import os

IMAGES_PER_BATCH = 100
TRAIN_PERCENTAGE = 0.75
VALID_PERCENTAGE = 0.20
TEST_PERCENTAGE = 0.05

TRAIN_IMAGES_PER_BATCH = int(IMAGES_PER_BATCH * TRAIN_PERCENTAGE)
VALID_IMAGES_PER_BATCH = int(IMAGES_PER_BATCH * VALID_PERCENTAGE)
TEST_IMAGES_PER_BATCH = IMAGES_PER_BATCH - (TRAIN_IMAGES_PER_BATCH + VALID_IMAGES_PER_BATCH)


def listname(path, train_path, valid_path, test_path):
    filelist = os.listdir(path)
    filelist.sort()

    with open(train_path, 'w') as f1, open(valid_path, 'w') as f2, open(test_path, 'w') as f3:
        total_files = len(filelist)
        train_written = 0
        valid_written = 0
        test_written = 0

        for i, files in enumerate(filelist):
            if files.endswith('.jpeg') or files.endswith('.jpg') or files.endswith('.png'):
                Olddir = os.path.join(path, files)
                if os.path.isdir(Olddir):
                    continue

                current_batch = i % IMAGES_PER_BATCH

                if current_batch < TRAIN_IMAGES_PER_BATCH:
                    f1.write(Olddir + '\n')
                    train_written += 1
                elif current_batch < TRAIN_IMAGES_PER_BATCH + VALID_IMAGES_PER_BATCH:
                    f2.write(Olddir + '\n')
                    valid_written += 1
                else:
                    f3.write(Olddir + '\n')
                    test_written += 1

    print(f"Training images: {train_written}, Validation images: {valid_written}, Test images: {test_written}")


savepath = os.getcwd()
train_path = os.path.join(savepath, "train.txt")
valid_path = os.path.join(savepath, "valid.txt")
test_path = os.path.join(savepath, "test.txt")

listname(os.path.join(savepath, "images"), train_path, valid_path, test_path)
print(f"train.txt, valid.txt, and test.txt have been created with the specified dataset split.")
